#!/bin/bash
jackhmmer --cpu 24 -N 8  --tblout sequence_result.tsv --domtblout sequence_domain.tsv data/SQ_degradation.fasta data/uhgp-100.fasta
