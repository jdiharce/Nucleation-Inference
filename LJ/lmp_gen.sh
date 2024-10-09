#!/bin/bash
#SBATCH --nodes=1
#SBATCH -n 32
#SBATCH --time=21:00:00
#SBATCH -J lammps066


# load modules
#. /etc/profile.d/modules.sh
 
#load appropriate modules1
module purge
module load lammps/2023.08.02/gcc-openmpi

cd /scratch/diharcej/LJ/
#cd $PBS_O_WORKDIR
srun lmp -in inputXXX.lmp
rm inputXXX.lmp
