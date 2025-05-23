#!/usr/bin/env python3
import os
import pandas as pd
import multiprocessing

path_to_files = 'HitsDir.GFF/FLGResult'
output_file = os.path.abspath(os.path.join(path_to_files, '../LocalGroups.tsv'))

# Получаем полные пути к файлам с нужным расширением
gff_files = [
    os.path.join(path_to_files, f) 
    for f in os.listdir(path_to_files) 
    if f.endswith('.groups.tsv')
]

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
    # Сначала собираем все данные
    with multiprocessing.Pool(processes=30) as pool:
        results = pool.map(extract_local_groups, gff_files)
    
    # Объединяем все результаты
    combined = pd.concat(results, ignore_index=True)
    
    # Записываем один раз
    combined.to_csv(output_file, sep='\t', index=False)