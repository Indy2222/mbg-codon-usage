#!/usr/bin/env python3

"""Analyze codon usage statistics.

Usage:
  analyze.py basic <stats-path> --ref-codon-usage <ref-path>
  analyze.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

import json
import os
import statistics
from collections import defaultdict
from itertools import product

from docopt import docopt


def main(arguments):
    if arguments['basic']:
        basic(arguments)


def basic(arguments):
    stats_path = arguments['<stats-path>']
    ref_path = arguments['<ref-path>']

    samples = load_samples(stats_path)

    with open(ref_path) as fp:
        ref_usage = json.load(fp)

    mean_codon_usage = compute_mean_codon_usage(samples)
    print_mean_codon_usage(mean_codon_usage)
    print_mean_abs_diff(mean_codon_usage, ref_usage)

    normalized = {
        population: {
            sample_name: normalize_triplets(sample['triplets'])
            for sample_name, sample in individuals.items()
        }
        for population, individuals in samples.items()
    }

    print_variances(normalized)


def print_variances(data):
    variances = {}
    for triplet in generate_triplets():
        variances[triplet] = statistics.variance(
            s[triplet] for p in data.values() for s in p.values())

    print_title('Individual Codon Usage Variances')
    print_triplet_table(variances, '{:10.6f}')


def print_mean_abs_diff(mean_codon_usage, ref_usage):
    diff_sum = 0
    for triplet in generate_triplets():
        diff_sum += abs(mean_codon_usage[triplet] - ref_usage[triplet])
    mean_abs_diff = diff_sum / 4**3

    print_title('Mean Absolute Deviation from Reference Codon Usage')
    print('{:.5f}'.format(mean_abs_diff))


def compute_mean_codon_usage(samples: dict) -> dict:
    codon_usage_sum = defaultdict(lambda: 0)
    for individuals in samples.values():
        for individual in individuals.values():
            for triplet, usage in individual['triplets'].items():
                codon_usage_sum[triplet] += usage
    return normalize_triplets(codon_usage_sum)


def print_mean_codon_usage(mean_codon_usage: dict):
    print_title('Mean Codon Usage')
    print_triplet_table(mean_codon_usage)


def print_triplet_table(data, fmt='{:4.1f}'):
    for first_symbol, second_symbol in product('ATCG', repeat=2):
        line = {}
        for third_symbol in 'ATCG':
            triplet = first_symbol + second_symbol + third_symbol
            line[triplet] = data[triplet]

        line = ' | '.join(k + ' | ' + fmt.format(v)
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


def generate_triplets():
    for triplet in product('ATCG', repeat=3):
        yield ''.join(triplet)


def print_title(title):
    print('\n' + title)
    print('=' * len(title) + '\n')


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
