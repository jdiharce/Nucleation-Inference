#!/bin/bash
#PBS -q beta
#PBS -l select=2:ncpus=24:mpiprocs=24
#PBS -l walltime=60:00:00
#PBS -N mytestjob
#PBS -j oe

## Use multiple of 2 with a maximum of 24 on 'ncpus' parameter, one node has 24 cores max
## With the 'select=3:ncpus=10:mpiprocs=10' option you get 30 cores on 3 nodes
## If you use select=1:ncpus=30 your job will NEVER run because no node has 30 cores.

# load modules
#. /etc/profile.d/modules.sh
 
#load appropriate modules
module purge
module load intel-compilers-18.0/18.0
module load intel/intel-cmkl-18.0/18.0
module load intel/intel-fc-18.0/18.0
module load intel/intel-mpi/2018.2
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/dev/intel/2018.release/compilers_and_libraries_2018.0.128/linux/tbb/lib/intel64_lin/gcc4.7
module load mpt/2.18

# Define an array of arguments
n_iter=5
Ts=('0.65' '0.66')
list_iter=('1000000' '5000000' '10000000') 
cvs=('s' 'e' 'aq6' 'q6')
dt=10
gauss_w=0.01

# Iterate over the arguments and run the script
for T in "${Ts[@]}"
    for cv in "${cvs[@]}"
        do
        for opt_iter in "${list_iter[@]}"
            do
                python3 makefile_opti.py --T $T --dt $dt --CV $cv --gauss_w $gauss_w --n_iter $opt_iter
                for ((i=0; i<$n_iter; i++))
                do
                    echo "../dt_study_${cv}/tresh=${tresh}_dt=${dt}_${i}"
                    ./optle 
                    cp PROFILES ../dt_study_${cv}/tresh=${tresh}_dt=${dt}_gw=${gauss_w}_${i}_${opt_iter}
                done
            done
    done
done
