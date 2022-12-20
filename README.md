# neurocor
A repository to calculate genetic correlations with brain imaging phenotypes hosted at https://open.win.ox.ac.uk/ukbiobank/big40/.

It uses snakemake to handle basic dependencies and workflow, and is configured for use with the slurm scheduler.

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

Make sure to set the name of your snakemake environment in the the script `run_cluster.sh` if you want to submit your jobs with slurm.

### Step 3
Configure your input files, see `config/input_sumstats.tsv`. If your input files have columns recognized by `ldsc/munge_sumstats.py`, the columns `PVAL_COLUMN`, `A1_COLUMN` and `A2_COLUMN` can be filled with placeholders ("."). You will need to define a sample-size `N` for every set of summary statistics. Variant-specific sample sizes are not yet supported.
### Step 4
Define which brain phenotypes you want to compute genetic correlations with by listing their identifiers in the file `config/big40_phenotypes.txt`. The default is to compare against all 3000+ phenotypes. A list of all phenotypes and their identifiers is contained in `resources/big40_metadata.tsv.gz` and online at https://open.win.ox.ac.uk/ukbiobank/big40/BIG40-IDPs_v4/IDPs.html/ (December 2021).
### Step 5
Trigger all steps by running

```
# check what whill be executed
bash run_cluster.sh --dry-run --quiet all
```

```
sbatch run_cluster.sh all
```

To follow pipeline progress:
```
tail -f snakemake*log
```

# S-LDSC enrichment

To run cell-type group analyses with [pre-computed annotations provided by the LDSC authors](https://github.com/bulik/ldsc/wiki/Cell-type-specific-analyses), you can choose one of the available cell type group sets, and request to run the analysis with the following command:

```
run_cluster.sh results/ldsc_cts/{id}/{ldcts_name}.ok
```

Where `{id}` should be substituted with the name of the phenotype defined in `config/input_sumstats.tsv` and `{ldcts_name}` is the name of the set of annotations you would like to estimate enrichments for. Available annotation sets are `Multi_tissue_gene_expr`, `Multi_tissue_chromatin`, `GTEx_brain`, `Cahoy`, `ImmGen`, or `Corces_ATAC`. Enrichments are calculated controling for the annotations in the "baseline ld" model using the HapMap3 variants, as defined by the ldsc authors. Please consider their documentation and [accompanying paper](https://www.nature.com/articles/s41588-018-0081-4) for details. 





