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
---
```
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
```

### 🔧 Script Descriptions

- [`amplicon_data_analysis.sh`](code/bin/amplicon_data_analysis.sh) — Bash script for processing amplicon variation data.
- [`bwa_samtools.sh`](code/bin/bwa_samtools.sh) — Bash pipeline for mapping reads using BWA and processing alignments with SAMtools.
- [`coverm.sh`](code/bin/coverm.sh) — Calculates RPKM values from read mappings for AGP locus coverage analysis (bash).
- [`DA_species_masline2.R`](code/bin/DA_species_masline2.R) — Builds a MASLiNE model for differential abundance of species (R).
- [`diamond.sh`](code/bin/diamond.sh) — Performs DIAMOND-based protein alignment (bash).
- [`exctractlocuses.py`](code/bin/exctractlocuses.py) — Extracts gene clusters with ±1000 bp flanks into FASTA format (adjustable).
- [`ExtractLocalGroup.py`](code/bin/ExtractLocalGroup.py) — Aggregates gene cluster DataFrames from `FindLocalGroup` output files into a single table (python).
- [`FindLocalGroup.py`](code/bin/FindLocalGroup.py) — Detects co-localized genes within a 5000 bp window and generates annotated GFF-style DataFrames (python).
- [`jackhmmer.sh`](code/bin/jackhmmer.sh) — Runs JackHMMER protein alignments against the target database (bash).
- [`phyl.R`](code/bin/phyl.R) — Infers phylogenetic relationships based on the identified gene clusters (R).


---

## ⚙️ Requirements

You can create the environment with:

```bash
conda env create -f environment.yml
conda activate sqd-analysis
```