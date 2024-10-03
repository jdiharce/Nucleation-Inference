directory=/scratch/diharcej/aimless-shooting/lammps_engine/AS_066/AS_trj

for trj in directory/*
do
	if [[ "$trj" == *fwd* && -f "$trj" ]]; then
		sed -i 's,'"MYSEED"','"$curr_seed"',g' commitor_loop.sh
		sbatch commitor_loop.sh
		break
	fi
done
