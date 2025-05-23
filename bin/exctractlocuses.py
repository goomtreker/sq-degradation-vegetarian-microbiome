#!/usr/bin/env python3
import os
import gzip
import pandas as pd
from io import StringIO
from multiprocessing import Pool
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

locus_info = pd.read_csv('locus_groups.csv') # 
output_dir = "locus_output"
os.makedirs(output_dir, exist_ok=True)

def extract_contig_from_gffgzfile(genome):
    subset = locus_info[locus_info['Genome'] == genome]
    gz_path = "HitsDir.GFF/gff_fasta/" + genome + '.gff.gz'
    with gzip.open(gz_path, "rt") as f:
        gff_content = f.read()

    fasta_start = gff_content.find("##FASTA")
    if fasta_start == -1:
        raise ValueError(f"No fasta in GFF file{genome}!")

    fasta_part = gff_content[fasta_start + len("##FASTA"):].strip()
    fasta_io = StringIO(fasta_part)
    records = SeqIO.to_dict(SeqIO.parse(fasta_io, "fasta"))
    records = {key: records[key] for key in subset['contig_id'].unique()}
    return records, subset

def extract_locus_worker(genome):
    try:
        records, subset = extract_contig_from_gffgzfile(genome)
        local_records = []

        for _, row in subset.iterrows():
            contig = records[row['contig_id']]
            seq_length = len(contig.seq)
            start = max(0, row['start'] - 1000)
            stop = min(seq_length, row['stop'] + 1000)
            locus_name = f"{row['contig_id']}:{start}:{stop} || {row['co_genes']} ||"
            locus = SeqRecord(
                contig.seq[start:stop],
                id=locus_name,
                description=f"Extracted from {contig.id}"
            )
            local_records.append(locus)

        # Save to individual FASTA file
        output_path = os.path.join(output_dir, f"{genome}_locuses.fasta")
        SeqIO.write(local_records, output_path, "fasta")
        print(f"[✓] Written: {output_path}")
    except Exception as e:
        print(f"[!] Error processing {genome}: {e}")

if __name__ == '__main__':
    with Pool(20) as pool:
        pool.map(extract_locus_worker, locus_info['Genome'].unique())

