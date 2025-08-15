#!/usr/bin/bash
#SBATCH -p gpu  # Partition
#SBATCH -G 1  # Number of GPUs
#SBATCH --ntasks=8                   # Number of CPU cores
#SBATCH --nodes=1                    # Number of nodes
#SBATCH --mem=3gb                    # Job memory request
#SBATCH --time=04:00:00              # Time limit hrs:min:sec
#SBATCH -o slurm-logs/%j-stdout.txt
#SBATCH -e slurm-logs/%j-stderr.txt
#SBATCH --mail-type=begin       # send email when job begins
#SBATCH --mail-type=end         # send email when job ends
#SBATCH --mail-user=andrea_pierre@student.uml.edu
#SBATCH --mail-type=TIME_LIMIT_80
#
#
## Activate env
module load conda/latest
conda config --add envs_dirs /work/pi_reza_azadeh_uml_edu/$USER/.conda/pkgs
conda config --add pkgs_dirs /work/pi_reza_azadeh_uml_edu/$USER/.conda/envs
mamba env create --file environment.yml
conda activate tGLAD
## Run script
python main.py
