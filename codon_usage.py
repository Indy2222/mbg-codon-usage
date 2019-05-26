#!/usr/bin/env python3

import json
import logging
import os
from itertools import product
from tempfile import TemporaryDirectory

from more_itertools import chunked

from cdnu.ccds import load_ccds
from cdnu.cram import load_cds_list
from cdnu.ftp import download_file_from_ftp
from cdnu.record import load_index

CHECKPOINT_FILE = 'checkpoint.txt'


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')

    # Number of already processed records.
    checkpoint = 0

    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as fp:
            checkpoint = int(fp.read())
            assert checkpoint >= 0
        logging.info('Checkpoint value / number of already process sequences'
                     ' is %d', checkpoint)
    else:
        logging.info('No checkpoint found, going to process all samples.')

    records = load_index('index.json')[checkpoint:]
    ccds_list = load_ccds()

    with TemporaryDirectory(prefix='mbg_codon_usage_') as tmp_dir:
        logging.info('Created temporary directory %s.', tmp_dir)

        for i, record in enumerate(records):
            logging.info('[%d/%d] Going to process sample %s...',
                         i + 1, len(records), record.sample_name)
            process_record(tmp_dir, record, ccds_list)

            # Store the checkpoint atomically.
            tmp_checkpoint = CHECKPOINT_FILE + '.tmp'
            with open(tmp_checkpoint, 'w') as fp:
                fp.write(str(i + checkpoint + 1))
            os.rename(tmp_checkpoint, CHECKPOINT_FILE)


def process_record(tmp_dir, record, ccds_list):
    seq_file_path = os.path.join(tmp_dir, 'seq.cram')
    index_file_path = seq_file_path + '.crai'

    logging.info('Going to download %s...', record.seq_url)
    download_file_from_ftp(record.seq_url, seq_file_path)
    logging.info('Going to download %s...', record.index_url)
    download_file_from_ftp(record.index_url, index_file_path)

    logging.info('Going to calculate codon usage statistics...')
    stats = {''.join(codon): 0 for codon in product('ATCG', repeat=3)}
    cds_list = load_cds_list(seq_file_path, ccds_list)

    processed_cds = 0
    for cds in cds_list:
        if cds is None:
            continue

        processed_cds += 1
        for triplet in chunked(cds, 3):
            if '-' in triplet or 'N' in triplet:
                continue
            stats[''.join(triplet)] += 1

    sample_json = {
        'triplets': stats,
        'numCds': len(cds_list),
        'numProcessedCds': processed_cds,
    }

    stats_file_name = record.sample_name + '.json'
    stats_file_dir = os.path.join('stats', record.population)
    stats_file_path = os.path.join(stats_file_dir, stats_file_name)

    if not os.path.exists(stats_file_dir):
        os.makedirs(stats_file_dir)

    logging.info('Sample has been processed, storing stats to %s...',
                 stats_file_path)
    with open(stats_file_path, 'w', encoding='utf-8', newline='\n') as fp:
        json.dump(sample_json, fp)


if __name__ == '__main__':
    main()
