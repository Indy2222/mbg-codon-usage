#!/usr/bin/env python3

from collections import defaultdict

from cdnu.ftp import download_ftp_text
from cdnu.record import Record, save_index

DATA_INDEX_URL = ('ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/'
                  '1000G_2504_high_coverage/'
                  '1000G_2504_high_coverage.sequence.index')
INDEX_FIELDS = (
    'ENA_FILE_PATH',
    'MD5SUM',
    'RUN_ID',
    'STUDY_ID',
    'STUDY_NAME',
    'CENTER_NAME',
    'SUBMISSION_ID',
    'SUBMISSION_DATE',
    'SAMPLE_ID',
    'SAMPLE_NAME',
    'POPULATION',
    'EXPERIMENT_ID',
    'INSTRUMENT_PLATFORM',
    'INSTRUMENT_MODEL',
    'LIBRARY_NAME',
    'RUN_NAME',
    'INSERT_SIZE',
    'LIBRARY_LAYOUT',
    'PAIRED_FASTQ',
    'READ_COUNT',
    'BASE_COUNT',
    'ANALYSIS_GROUP'
)


def main():
    records = load_index()
    # This is important to have populations evenly represented even if we
    # process only part of them.
    records = reorder_index(records)
    save_index('index.json', records)


def reorder_index(records):
    """Order records so individuals from different populations are
    intermixed."""
    populations = defaultdict(lambda: [])
    for record in records:
        populations[record.population].append(record)

    sorted_records = []
    while populations:
        # Call list() on the keys so we can change the dict inside the loop.
        for population_name in list(populations.keys()):
            sorted_records.append(populations[population_name].pop())
            if not populations[population_name]:
                del populations[population_name]

    return sorted_records


def load_index():
    """Download sequence index, parse it and return a list of
    :class:`Record`."""
    index_str = download_ftp_text(DATA_INDEX_URL)
    records = (
        {INDEX_FIELDS[i]: v for i, v in enumerate(l.split('\t'))}
        for l in index_str.split('\n') if l and not l.startswith('#')
    )

    return [
        Record(
            seq_url=record['ENA_FILE_PATH'],
            index_url='{}.crai'.format(record['ENA_FILE_PATH']),
            sample_name=record['SAMPLE_NAME'],
            population=record['POPULATION']
        )
        for record in records
    ]


if __name__ == '__main__':
    main()
