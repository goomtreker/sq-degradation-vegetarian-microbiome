#!/bin/bash

# Script for mmseq clustering
THREADS=24
min_seq_ids=(0.95 0.75 0.5)
coverages=(0.8 0.5)

for min_id in "${min_seq_ids[@]}"; do
  for cov in "${coverages[@]}"; do
    outname="SQDdb_clu_id${min_id}_cov${cov}"
    tmpdir="tmp_id${min_id}_cov${cov}"
    echo "Кластеризация: --min-seq-id $min_id -c $cov"
    mmseqs cluster SQD_locus.db "$outname" "$tmpdir" --min-seq-id "$min_id" --cov-mode 0 -c "$cov" --threads $THREADS
  done
done