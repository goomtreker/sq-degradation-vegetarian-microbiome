# SQ Degradation Pathway Analysis in Human Gut Microbiome

This pipeline identifies and characterizes microbial enzymes and gene clusters involved in **sulfoquinovose (SQ) degradation** across gut microbiomes of vegetarians and non-vegetarians.

It integrates HMMER, DIAMOND, genome annotations, and pathway reconstruction to detect and visualize conserved metabolic loci.

---

## 🧪 Project Highlights

- Uses **DIAMOND** and **JackHMMER** to find homologs of SQ-degrading enzymes in the **UHGP** database.
- Annotates gene hits with pathway and taxonomic information.
- Groups enzymes into **co-located loci** using GFF annotation.
- Detects **core metabolic pathways** (EMP, TK, TAL, ED).
- Performs **visualization** and **OLS statistical modeling** of pathway abundance.

---

## 📁 Directory Structure

./
├── code
│   ├── bin
│   │   ├── amplicon_data_analysis.sh
│   │   ├── bwa_samtools.sh
│   │   ├── coverm.sh
│   │   ├── DA_species_masline2.R
│   │   ├── diamond.sh
│   │   ├── exctractlocuses.py
│   │   ├── ExtractLocalGroup.py
│   │   ├── FindLocalGroup.py
│   │   ├── jackhmmer.sh
│   │   └── phyl.R
│   └── SQDegradationAnalysis.ipynb
├── data
│   └── metadata_rpkm.csv
├── environment.yml
└── README.md
