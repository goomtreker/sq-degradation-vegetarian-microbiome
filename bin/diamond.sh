diamond makedb --in uhgp-100.faa  --db uhgp-100

diamond blastp --masking none --sensitive -f 6 --db /home/aanurov/beegfs/SQ_project/uhgp-100.dmnd --query ../SQ_degradation.fasta --out SQD_uhgp100.tsv --threads 24
