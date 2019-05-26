from cdnu.ccds import CdsPos, load_ccds
from cdnu.cram import load_cds_list


def test_load_cds_list():
    cds = load_cds_list('./test/cramExample.cram',
                        [CdsPos('first', [(33036411, 33036588)], '21')])
    assert len(cds) is 1
    single_cds = cds[0]
    assert single_cds is not None
    assert len(single_cds) % 3 is 0
    assert len(single_cds) is (33036588 - 33036411)
    assert single_cds.startswith('ATG')
    assert single_cds[-3:] in ('TAG', 'TAA', 'TGA')


def test_load_cds_list_small():
    cds = load_cds_list('./test/cramExample.cram',
                        [CdsPos('first', [(33036660, 33036670)], '21')])
    assert len(cds) is 1
    assert cds[0] is None


def test_load_cds_list_some():
    ccds = [
        CdsPos('first', [(925941, 926012)], 'chr1'),
        CdsPos('second', [(966531, 966613)], 'chr1'),
        CdsPos('third', [(7784877, 7785004)], 'chr1')
    ]
    address = ('ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/'
               '1000G_2504_high_coverage/data/ERR3239281/NA07051.final.cram')
    address = '/Users/peta/School/mbg/mbg-codon-usage/huge/NA07051.final.cram'

    cds_list = load_cds_list(address, ccds)

    assert len(cds_list) is 3
    assert cds_list[0] is None
    assert cds_list[1] is None
    assert cds_list[2] is None


def test_load_cds_list_huge():
    ccds = load_ccds()
    address = ('ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/'
               '1000G_2504_high_coverage/data/ERR3239281/NA07051.final.cram')
    address = '/Users/peta/School/mbg/mbg-codon-usage/huge/NA07051.final.cram'

    cds_list = load_cds_list(address, ccds[:100])

    for cds in cds_list:
        if cds is not None:
            print('{}.. {:4} ..{}'.format(cds[:3], len(cds), cds[-3:]))
            assert len(cds) % 3 is 0
            assert cds.startswith('ATG')
            assert cds[-3:] in ('TAG', 'TAA', 'TGA')
        else:
            print('None')
