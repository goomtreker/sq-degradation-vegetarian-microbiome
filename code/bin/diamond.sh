#!/bin/bash
diamond makedb --in uhgp-100.faa  --db uhgp-100

diamond blastp --masking none --sensitive -f 6 --db data/uhgp-100.dmnd --query data/SQ_degradation_enzymes.fasta --out SQD_uhgp100.tsv --threads 24
