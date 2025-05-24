#!/bin/bash
jackhmmer --cpu 24 -N 8  --tblout data/sequence_result.tsv --domtblout data/sequence_domain.tsv data/SQ_degradation.fasta data/uhgp-100.fasta
