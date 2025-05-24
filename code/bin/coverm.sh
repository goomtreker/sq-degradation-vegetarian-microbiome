#!/bin/bash
split -l 10 bai_list.txt bam_batch_

WORK_DIR="$PWD"

for bam_batch_file in "$WORK_DIR"/bam_batch_*; do
  base_name="${bam_batch_file}"
  bam_files=$(cat "$bam_batch_file" | tr '\n' ' ')
  coverm contig -m rpkm -t 10 --min-read-percent-identity 95 --min-read-aligned-percent 50 --proper-pairs-only --bam-files $bam_files -o "${base_name}_95_50.tsv"
done
