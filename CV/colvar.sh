#!/bin/bash
#SBATCH --nodes=1
#SBATCH -n 32
#SBATCH --time=1:00:00
#SBATCH -J colvar

#load appropriate modules1
module purge
module load lammps/2023.08.02/gcc-openmpi


lmp_data=/store/diharcej/LJ/data2.lmp
lmp_trj=/store/diharcej/LJ/0.64_trj/last_trj/last_dump21346.lammpstrj 

directory=/store/diharcej/0.65_trj
#mkdir $directory/e_colvar
for file in "$directory"/*; do
    # Check if the file contains 'test' in its name and is a regular file
    if [[ "$file" == *dump* && -f "$file" ]]; then
        # Extract the filename without the directory path
        filename=$(basename "$file")
        echo $filename
	echo $file
	filename="$directory/e_colvar/$filename"
 	sed 's,'"MYTRJ"','"$file"',g' compute_e_gen.lmp > compute_e.lmp
	sed -i 's,'"NAME"','"$filename"',g' compute_e.lmp
	srun lmp -in compute_e.lmp
    fi
done
