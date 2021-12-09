# neurocor
A repository to calculate genetic correlations with brain imaging phenotypes hosted at https://open.win.ox.ac.uk/ukbiobank/big40/.

It uses snakemake to handle basic dependencies and workflow, and us configured for use with the slurm scheduler.

## Setup
### Step 1
Clone the repository. In the base directory, run `install.sh`.
```
bash install.sh
```
### Step 2
Install snakemake
```
conda create -n snakemake -c conda-forge mamba && conda activate snakemake && mamba install -c bioconda -c conda-forge snakemake
```
### Step 3
Configure your input files, see `conf/input_sumstats.tsv`. If you're input files have columns recognized by `ldsc/munge_sumstats.py`, the columns `PVAL_COLUMN`, `A1_COLUMN` and `A2_COLUMN` can be filled with placeholders ("."). You will need to define a sample-size `N` for every set of summary statistics. Variant-specific sample sizes are not yet supported.
### Step 4
Define which brain phenotypes you want to compute genetic correlations with by listing their identifiers in the file `config/big40_phenotypes.txt`. The default is to compare against all 3000+ phenotypes. A list of all phenotypes and their identifiers is contained in `resources/big40_metadata.tsv.gz` and online at https://open.win.ox.ac.uk/ukbiobank/big40/BIG40-IDPs_v4/IDPs.html/ (December 2021).
### Step 5
Trigger all steps by running
```
...
```
