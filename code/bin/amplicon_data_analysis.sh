wget https://figshare.com/ndownloader/files/11070320

# import biom file to the QIIME2
qiime tools import \ 
  --input-path deblur_125nt_no_blooms.biom \ # file for import to biom format
  --type 'FeatureTable[Frequency]' \ 
  --input-format BIOMV210Format \ 
  --output-path agp_counts.qza 

# filtration feature-table by diet in metadata
qiime feature-table filter-samples \ 
  --i-table agp_counts.qza \
  --m-metadata-file ../data/metadata_filter_o_v.csv \ 
  --o-filtered-table filtered_agp_counts.qza

# taxa collapse
  qiime2-amplicon-2024.10.sif \
  qiime taxa collapse \
  --i-table agp_counts_asv.qza \
  --i-taxonomy ../data/taxonomy.qza \
  --p-level 6 \
  --o-collapsed-table collapsed_agp_table.qza

# ancom-bc
   qiime composition ancombc \
  --i-table collapsed_agp_table.qza \
  --m-metadata-file ../data/metadata_filter_o_v.csv \
  --p-formula "diet_type" \
  --p-p-adj-method 'bonferroni' \
  --p-prv-cut 0.1 \
  --p-lib-cut 1 \
  --p-tol 1e-05 \
  --p-max-iter 1000 \
  --p-no-conserve \
  --p-alpha 0.05 \
  --o-differentials agp-ancombc-subject.qza \
  --verbose 2>&1 | tee detailed.log
  
