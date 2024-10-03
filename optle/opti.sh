#!/bin/bash
#SBATCH --job-name=my_fortran_job
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#SBATCH --partition=your_partition
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00

# Define an array of arguments
n_iter=5
Ts=('0.65' '0.66')
list_iter=('5000000' '10000000') 
cvs=('s' 'e' 'q6')
dt=10
gauss_w=0.01

# Iterate over the arguments and run the script
for opt_iter in "${list_iter[@]}"
    do
    for T in "${Ts[@]}"
        do
        for cv in "${cvs[@]}"
            do
                python3 makefile_opti.py --T $T --dt $dt --CV $cv --gauss_w $gauss_w --n_iter $opt_iter
                for ((i=0; i<$n_iter; i++))
                do
                    echo "../dt_study_${cv}/tresh=${tresh}_dt=${dt}_${i}"
                    ./optle 
                    cp PROFILES ../opt_T${T}_${cv}/dt=${dt}_gw=${gauss_w}_${i}_${opt_iter}
                done
            done
        done
    done
