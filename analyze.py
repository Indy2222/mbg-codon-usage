#!/usr/bin/env python3

"""Analyze codon usage statistics.

Usage:
  analyze.py basic <stats-path>
  analyze.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

import json
import os
from collections import defaultdict
from itertools import product

from docopt import docopt


def main(arguments):
    if arguments['basic']:
        basic(arguments)


def basic(arguments):
    stats_path = arguments['<stats-path>']
    samples = load_samples(stats_path)

    mean_codon_usage = compute_mean_codon_usage(samples)
    print_mean_codon_usage(mean_codon_usage)


def compute_mean_codon_usage(samples: dict) -> dict:
    codon_usage_sum = defaultdict(lambda: 0)
    for individuals in samples.values():
        for individual in individuals.values():
            for triplet, usage in individual['triplets'].items():
                codon_usage_sum[triplet] += usage
    return normalize_triplets(codon_usage_sum)


def print_mean_codon_usage(mean_codon_usage: dict):
    print('Mean Codon Usage')
    print('================\n')

    for first_symbol, second_symbol in product('ATCG', repeat=2):
        line = {}
        for third_symbol in 'ATCG':
            triplet = first_symbol + second_symbol + third_symbol
            line[triplet] = mean_codon_usage[triplet]

        line = ' | '.join(k + ' | ' + '{:4.1f}'.format(v)
                          for k, v in line.items())
        print('| ' + line + ' |')


def normalize_triplets(triplets):
    total_triplets = sum(triplets.values())
    return {k: 1000 * v / total_triplets for k, v in triplets.items()}


def load_samples(stats_path: str) -> dict:
    samples = defaultdict(lambda: {})

    for dirpath, dirnames, filenames in os.walk(stats_path):
        _, population = os.path.split(dirpath)
        for filename in filenames:
            with open(os.path.join(dirpath, filename)) as fp:
                sample_name, _ = os.path.splitext(filename)
                samples[population][sample_name] = json.load(fp)

    # Convert to dict
    return dict(samples)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
