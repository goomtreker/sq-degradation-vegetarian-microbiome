#!/bin/bash
jackhmmer --cpu 24 -N 8  --tblout data/sequence_result.tsv --domtblout data/sequence_domain.tsv data/data/SQ_degradation_enzymes.fasta data/uhgp-100.fasta
