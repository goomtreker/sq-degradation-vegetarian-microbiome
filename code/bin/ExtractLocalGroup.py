#!/usr/bin/env python3
import os
import pandas as pd
import multiprocessing
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract clusters to one file')
    parser.add_argument('-i', '--input-dir', required=True, 
                        help='Path to FLGResult directory containing .groups.tsv files')
    parser.add_argument('-o', '--output-file', 
                        help='Output file path (default: <input_dir>/../LocalGroups.tsv)')
    parser.add_argument('-p', '--processes', type=int, default=2,
                        help='Number of parallel processes to use (default: 2)')
    return parser.parse_args()

def extract_local_groups(path_to_df: str) -> None:
    try:
        tmp = pd.read_csv(path_to_df, sep='\t')
        tmp = tmp[tmp['co_genes'].notna()]
        tmp['Genome'] = os.path.basename(path_to_df).replace('.groups.tsv', '')
        return tmp
    except Exception as e:
        print(f"Error processing {path_to_df}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Set output file path
    if args.output_file:
        output_file = os.path.abspath(args.output_file)
    else:
        output_file = os.path.abspath(os.path.join(args.input_dir, '../LocalGroups.tsv'))

    # Get full paths to all .groups.tsv files
    gff_files = [
        os.path.join(args.input_dir, f) 
        for f in os.listdir(args.input_dir) 
        if f.endswith('.groups.tsv')
    ]
    
    # Load all DataFrames in parallel
    with multiprocessing.Pool(processes=args.processes) as pool:
        results = pool.map(extract_local_groups, gff_files)

    # Concatenate all partial results into one DataFrame
    combined = pd.concat(results, ignore_index=True)

    # Save the final merged dataframe once
    combined.to_csv(output_file, sep='\t', index=False)
    print(f"Results saved to {output_file}")
