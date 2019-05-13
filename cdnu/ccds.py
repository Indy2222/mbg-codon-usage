from typing import List, NamedTuple

CCDS_FILE = 'CCDS.current.txt'
CHROMOSOMES = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
               '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
               'X', 'Y')


class CdsPos(NamedTuple):

    ccds_id: str
    indexes: list
    """2-tuples with start (inclusive) and stop indexes (exclusive) in
    reference genome. Whole CDS can be constructed as concatenation of the
    sub-sequences."""
    chromosome: str
    """Chromosome name, see :const:`CHROMOSOMES`"""



def load_ccds() -> List[List[tuple]]:
    """Load file with CDS locations within GRCh38 genome as a list of
    :class:`CdsPos`."""
    cds = []

    with open(CCDS_FILE, encoding='utf-8', newline='\n') as fp:
        for line in fp:
            if not line:
                # Skip empty lines
                continue
            if line.startswith('#'):
                # Skip comments
                continue

            parts = line.split('\t')

            ccds_id = parts[4]
            status = parts[5]
            if 'Public' not in status:
                # CDS is not yet public
                continue

            locations_str = parts[9]
            if locations_str == '-':
                # CDS location unknown
                continue

            chromosome = parts[0]
            assert chromosome in CHROMOSOMES, chromosome

            locations = []
            assert locations_str.startswith('[')
            assert locations_str.endswith(']')
            for location_str in locations_str[1:-1].split(','):
                start_str, stop_str = location_str.split('-')
                start, stop = int(start_str), int(stop_str) + 1
                locations.append((start, stop))

            if sum(b - a for a, b in locations) % 3 != 0:
                # Skip CDS which are not multiple of three in length.
                continue

            cds.append(CdsPos(
                ccds_id=ccds_id,
                chromosome=chromosome,
                indexes=locations
            ))

    return cds
