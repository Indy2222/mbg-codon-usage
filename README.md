Codon Usage
===========

This repository is trying to investigate differences in codon usage among
various H. Sapiens populations. We are using data from
[1000 Genomes Project](http://www.internationalgenome.org/) for this purpose.

License
-------

See [LICENSE](/LICENSE).

Repository Structure
--------------------

* [**/analyze.py**](/analyze.py) – this scripts produces various statistics and
  statistical tests over data produced by `codon_usage.py`.

* [**/CCDS.current.txt**](/CCDS.current.txt) –
  [Current Consensus CDS](https://www.ncbi.nlm.nih.gov/projects/CCDS/CcdsBrowse.cgi)
  as downloaded from ftp://ftp.ncbi.nlm.nih.gov/pub/CCDS/current_human.

* [**/download_index.py**](/download_index.py) – this script downloads and
  stores index of available whole genome samples from
  [NCBI](https://www.ncbi.nlm.nih.gov/) server and stores the result to a JSON
  file.

* [**/codon_usage.py**](/codon_usage.py) – this script downloads whole genome
  CRAM file and produces codon usage statistics for each individual in an index
  file (see `download_index.py`).

* [**/reference_codon_usage.json**](/reference_codon_usage.json) – codon usage
  downloaded from
  https://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=9606 and
  normalized to values between 0 and 1.

* [**/report**](/report) – final report of our findings written in LaTeX.
