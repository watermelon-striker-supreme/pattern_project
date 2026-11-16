#!/bin/bash
#SBATCH --job-name=Mutation_Detect
#SBATCH --array=1-500%100
#SBATCH --time=00:05:00
#SBATCH --mem=1G
#SBATCH --output=logs/mutation_%A_%a.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate pattern_env

python src/worker.py $SLURM_ARRAY_TASK_ID