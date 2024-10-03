#!/bin/bash
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH -n 32
#SBATCH -J q6_065


python ComputeQ6.py --T 0.66
