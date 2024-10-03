#!/bin/bash
dir_trj=/store/diharcej/LJ/0.64_trj/last_trj
frame=600

for trj in $dir_trj/*
do
	if [[ "$trj" == *lammpstrj* && -f "$trj" ]]; then	
		echo $trj
		timestep=$(sed '2q;d' $trj)
		conf=$((timestep + frame * 100))
	        output=$(basename "$trj")
		output=$(echo "$output" | cut -d'.' -f1)
		mkdir AS_trj/$output
		mkdir AS_trj/$output/AS_trj
		sed 's,'"INITRJ"','"$trj"',g' AS_loop.sh > ./AS_trj/$output/AS_loop.sh
		sed -i 's,'"INICONF"','"$conf"',g' ./AS_trj/$output/AS_loop.sh
		cp ./in_bwd.lmp ./AS_trj/$output/
		cp ./in_fwd.lmp ./AS_trj/$output/
		cd ./AS_trj/$output
		sbatch ./AS_loop.sh
		cd ../../
	fi	
done





