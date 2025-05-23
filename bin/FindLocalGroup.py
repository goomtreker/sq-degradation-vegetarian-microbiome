#!/usr/bin/env python3
import pandas as pd
from re import search
import os
from numpy import nan
import sys
import multiprocessing



def parse_gff_to_pandas(gff_file):
    gff_annots = pd.read_csv(gff_file, 
                         compression='gzip', 
                         sep='\t', 
                         comment='#',
                         usecols=[0, 3, 4, 6, 8],
                         names = ['genome_region', 'start', 'stop', 'strand', 'features'],
                         engine='python')
    seq_index = gff_annots['genome_region'].str.contains('>').idxmax()
    gff_annots = gff_annots.loc[:seq_index - 1]
    return gff_annots


def co_localization(group, window=5000):
    group = group.copy()

    group["midpoint"] = (group["start"] + group["stop"]) / 2

    group.loc[group['gene_name'].notna(),"tmp_groups"] = (group.loc[group['gene_name'].notna(), "midpoint"]
     - group.loc[group['gene_name'].notna(), "midpoint"].shift(1) > window).cumsum()

    group["co_genes"] = (
        group.groupby("tmp_groups")["gene_name"]
        .transform(lambda x: ", ".join(x.dropna().unique()) if len(x.dropna().unique()) > 1 else nan)
                        )

    group = group.drop(columns=['tmp_groups'])
    return group


def find_groups(gff_file, hits_table):
    genome = search(r'\w+', os.path.basename(gff_file))
    gff_dataframe = parse_gff_to_pandas(gff_file)
    gff_dataframe['protein_id'] = gff_dataframe['features'].str.extract(r"ID=(MGYG\d+_\d+)")
    gff_hits = hits_table[hits_table['Genome'] == genome[0]].set_index('hit_id')['gene_name'].to_dict()
    gff_dataframe['gene_name'] = gff_dataframe['protein_id'].map(gff_hits)
    result_list = []
    for name, group in gff_dataframe.groupby('genome_region'):
        processed_group = co_localization(group)
        processed_group["genome_region"] = name
        result_list.append(processed_group)

    result = pd.concat(result_list, ignore_index=True)

    return result


def process_file(gff_file, hits_table):
    result = find_groups(gff_file, hits_table)
    genome = search(r'\w+', os.path.basename(gff_file))[0]
    os.makedirs("FLGResult", exist_ok=True)
    result.to_csv(os.path.join("FLGResult", genome + '.groups.tsv'), index=False, sep='\t')

if __name__ == "__main__":
    hits_table = pd.read_csv(sys.argv[1])  
    gff_folder = sys.argv[2]               
    cpus = int(sys.argv[3])                

    gff_files = [os.path.join(gff_folder, f) for f in os.listdir(gff_folder) if f.endswith(".gff.gz")]

    with multiprocessing.Pool(processes=cpus) as pool:
        pool.starmap(process_file, [(gff, hits_table) for gff in gff_files])
