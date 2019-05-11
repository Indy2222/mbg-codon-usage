Codon Usage
===========

This repository is trying to investigate differences in codon usage among
various H. Sapiens populations and H. neanderthalensis. We are using data from
[1000 Genomes Project](http://www.internationalgenome.org/) and
[genome sequence of a Neandertal from the Altai Mountains](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4031459/)
for this purpose.


Repository Structure
--------------------

* [**/CCDS.current.txt**](/CCDS.current.txt) –
  [Current Consensus CDS](https://www.ncbi.nlm.nih.gov/projects/CCDS/CcdsBrowse.cgi)
  as downloaded from ftp://ftp.ncbi.nlm.nih.gov/pub/CCDS/current_human.

* [**/download_index.py**](/download_index.py) – this script downloads and
  stores index of available whole genome samples from
  [NCBI](https://www.ncbi.nlm.nih.gov/) server and stores the result to a JSON
  file.
