#!/usr/bin/env python3
import os
import pandas as pd
import argparse
import multiprocessing
from re import search
from numpy import nan


def parse_gff_to_pandas(gff_file):
    gff_annots = pd.read_csv(
        gff_file,
        compression='gzip',
        sep='\t',
        comment='#',
        usecols=[0, 3, 4, 6, 8],
        names=['genome_region', 'start', 'stop', 'strand', 'features'],
        engine='python'
    )
    seq_index = gff_annots['genome_region'].str.contains('>').idxmax()
    gff_annots = gff_annots.loc[:seq_index - 1]
    return gff_annots


def co_localization(group, window=5000):
    group = group.copy()
    group["midpoint"] = (group["start"] + group["stop"]) / 2
    group.loc[group['gene_name'].notna(), "tmp_groups"] = (
        group.loc[group['gene_name'].notna(), "midpoint"]
        .diff()
        .gt(window)
        .cumsum()
    )
    group["co_genes"] = group.groupby("tmp_groups")["gene_name"].transform(
        lambda x: ", ".join(x.dropna().unique()) if len(x.dropna().unique()) > 1 else nan
    )
    return group.drop(columns=['tmp_groups'])


def find_groups(gff_file, hits_table):
    genome = search(r'\w+', os.path.basename(gff_file)).group()
    gff_dataframe = parse_gff_to_pandas(gff_file)
    gff_dataframe['protein_id'] = gff_dataframe['features'].str.extract(r"ID=(MGYG\d+_\d+)")
    gff_hits = hits_table[hits_table['Genome'] == genome].set_index('hit_id')['gene_name'].to_dict()
    gff_dataframe['gene_name'] = gff_dataframe['protein_id'].map(gff_hits)

    result_list = []
    for name, group in gff_dataframe.groupby('genome_region'):
        processed_group = co_localization(group)
        processed_group["genome_region"] = name
        result_list.append(processed_group)

    return pd.concat(result_list, ignore_index=True)


def process_file(gff_file, hits_table):
    result = find_groups(gff_file, hits_table)
    genome = search(r'\w+', os.path.basename(gff_file)).group()
    os.makedirs("FLGResult", exist_ok=True)
    result.to_csv(os.path.join("FLGResult", f"{genome}.groups.tsv"), index=False, sep='\t')


def main():
    parser = argparse.ArgumentParser(
        description="Find co-localized gene groups from GFF annotations and hit table."
    )
    parser.add_argument("hits_table", help="Path to hits.csv file containing 'hit_id', 'Genome', and 'gene_name' columns.", required=True)
    parser.add_argument("gff_folder", help="Directory with .gff.gz annotation files.", required=True)
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of parallel threads (default: 4)")
    parser.add_argument("-w", "--window", type=int, default=5000,
                        help="Window size in base pairs for gene co-localization (default: 5000)")

    args = parser.parse_args()

    hits_table = pd.read_csv(args.hits_table)
    gff_files = [os.path.join(args.gff_folder, f) for f in os.listdir(args.gff_folder) if f.endswith(".gff.gz")]
    window = args.window

    with multiprocessing.Pool(processes=args.threads) as pool:
        pool.starmap(process_file, [(gff, hits_table, window) for gff in gff_files])


if __name__ == "__main__":
    main()
