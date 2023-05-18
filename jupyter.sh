#!/bin/bash -eux
#SBATCH --job-name=jupyter_%j
#SBATCH --output=jupyter_%j.out
#SBATCH --partition=hpcpu,vcpu # -p
#SBATCH --cpus-per-task=1 # -c
#SBATCH --mem=6gb
#SBATCH --time=8:00:00 # 5 minutes  
 
# Initialize conda:
eval "$(conda shell.bash hook)"
 
if [ "$#" -eq 0 ]; then
	port=60000
else
	port=$1
fi

# some command to activate a specific conda environment or whatever:
conda activate base

jupyter-lab --port=$port
