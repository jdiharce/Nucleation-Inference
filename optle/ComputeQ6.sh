#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH -n 32
#SBATCH -J q6_066


python3 ComputeQ6.py --T 0.65
