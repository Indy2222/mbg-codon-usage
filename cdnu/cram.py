from typing import List, Optional

from pysam import AlignmentFile

from cdnu.ccds import CdsPos


def load_cds_list(cram_file_path: str, cds_list: List[CdsPos]) -> List[str]:
    """Load CDS sequences (:param:`cds_list`) from a CRAM file
    (:param:`cram_file_path`). The CRAM file should be whole Homo Sapiens
    genome aligned to GRCh38 reference assembly.

    A list of CDS strings is returned. "Candidate" CDS not starting with "ATG"
    are replaced by None.
    """
    with AlignmentFile(cram_file_path, 'rc') as cram:
        assert cram is not None
        cds_strings = [find_single_cds(cram, cds_seq) for cds_seq in cds_list]
    return remove_invalid_cds(cds_strings)


def find_single_cds(cram: AlignmentFile, sequence_cds: CdsPos) -> str:
    """ Finds (presumed) cds sequence by parameters

    :param cram: pre-loaded file to be search
    :param sequence_cds: CDS location

    :return: a string with DNA symbols A, T, C, G
    """
    single_cds = ''

    size = 0
    # The CDS be spliced from multiple exons.
    for cds_from, cds_to in sequence_cds.indexes:
        assert cds_from is not None
        assert cds_to is not None
        size += cds_to - cds_from

        region = '{}:{}-{}'.format(sequence_cds.molecule, cds_from, cds_to)
        index = cds_from
        for read in cram.fetch(region=region):
            if read.reference_start is None or read.reference_end is None:
                continue
            ref_from = read.positions[0]
            ref_to = read.positions[-1]
            assert ref_from is not None
            assert ref_to is not None

            if ref_from > index:
                missing_len = ref_from - index
                single_cds += '-' * missing_len
                index += missing_len

            if ref_from <= index < ref_to and index <= cds_to + 1:
                read_start = max(cds_from, index) - ref_from
                read_end = min(cds_to, ref_to) - ref_from
                single_cds += read.seq[read_start:read_end]
                index += read_end - read_start

            if index > cds_to:
                break

        # Fill missing remainder (if any) with -.
        single_cds += '-' * (size - len(single_cds))

    return single_cds


def remove_invalid_cds(cds_list: List[str]) -> List[Optional[str]]:
    """This function replaces coding sequences which doesn't start with ATG
    or end with one of TAG, TAA or TGA with None-s."""
    return [
        t if t[:3] == 'ATG' and t[-3:] in ('TAG', 'TAA', 'TGA') else None
        for t in cds_list
    ]
