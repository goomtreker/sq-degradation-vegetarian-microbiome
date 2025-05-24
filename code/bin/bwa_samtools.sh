#!/bin/bash
bwa index SQD_locus_for_mapping.fasta

WORKDIR="$PWD"
SQD_LOCUS="${WORKDIR}/SQD_locus_for_mapping.fasta"
SAM_DIR1="${WORKDIR}/SQD_locus_SAM"
INPUT_DIR="${WORKDIR}/Microbiome_part/agp_wgs_balanced"


for r1_file in "$INPUT_DIR"/*.R1.fastq.gz; do
  base_name=$(basename "$r1_file" .R1.fastq.gz)
  r2_file="$INPUT_DIR/$base_name.R2.fastq.gz"
  if [[ -f "$r2_file" ]]; then
    echo "Processing $base_name..."
    bwa mem -t 10 "$SQD_LOCUS" "$r1_file" "$r2_file" > "$SAM_DIR1/${base_name}.sam"
  else
    echo "Warning: Pair for $r1_file not found!" >&2
  fi
done

SAM_DIR2="${WORKDIR}/SQD_locus_SAM"

for sam_file in "$SAM_DIR2";do
  base_name="${sam_file%.sam}"
  samtools view -bS "$sam_file" | samtools sort -o "${base_name}.sorted.bam"
  samtools index "${base_name}.sorted.bam"
done
