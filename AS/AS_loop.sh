#!/bin/bash -l

# This is the aimless shooting submission script

#========================================
#!/bin/bash
#SBATCH --nodes=1
#SBATCH -n 32
#SBATCH --time=21:00:00
#SBATCH -J AS065


module purge
module load lammps/2023.08.02/gcc-openmpi

base_dir=$(pwd)
echo $base_dir

# Aimless shooting parameters

max_length_fwd=30000
max_length_bwd=30000
init_iter=200
as_step_ini=200
as_step=100
max_step=1
max_iter=1500
lmp_data=/scratch/diharcej/aimless-shooting/lammps_engine/LJ/data2.lmp
ini_trj=/scratch/diharcej/aimless-shooting/lammps_engine/AS_065/accepted_trj_300/bwd_iter_000192.lammpstrj
#ini_conf=3177000
#ini_conf=26339600
ini_conf=400
echo "Aimless shooting timestep: $delta_t MD steps"

# Returns the basin committment of a run
# Argument: plumed output file

trajectory_status() {
  #grep "TIMESTEP" $1 | tail -1
  #tail -n 100 $1
  #local line=$(tail -n 4008 $1 | head -n 1)
  local line=$(sed '2q;d' $1)
  echo $line
}

# Tests if trajectory connects basins A and B
# Argument: current work dir

is_connected() {
  local bwd_status=$(trajectory_status $1/bwd/last_lammpstrj)
  local fwd_status=$(trajectory_status $1/fwd/last_lammpstrj)
  if [[ "$bwd_status" -ne "$max_length_bwd" && "$fwd_status" -ne "$max_length_fwd" ]]; then
    connected='True'
  else
    connected='Fasle'
  fi
  echo $connected
}

# Flips a coin to return a shooting point
# New shooting point is either + or - dt
draw_shooting_point_flip() {
  local coin_flip=$(($RANDOM%2)) 
  if [ $coin_flip -eq 0 ] ; then
    local result="bwd"
  else
    local result="fwd"
  fi
  echo $result
}

# Three outcomes to return a shooting point
# New shooting point is either current or + or - dt
draw_shooting_point() {
  local coin_flip=$((RANDOM % (2 * max_step + 1) - max_step))
  echo $coin_flip
}

# Begin the aimless shooting loop

#mkdir accepted_trj_${as_step}
mkdir AS_trj
acc=0
rej=0
tot=0

a=0
last_accepted=$ini_trj
accepted="False"

echo "# iter Nacc Nrej Ntot AcceptanceRatio" >> statistics.txt

while [ $a -lt $max_iter ] ; do

  iter_dir=iter_$(printf "%06d" $a)
  mkdir $iter_dir

  cd ${base_dir}/${iter_dir}

  # In the next steps, edit the lammps submission
  # script according to current state

  mkdir bwd
  mkdir fwd

  cp ${base_dir}/in_bwd.lmp ${base_dir}/${iter_dir}/bwd/in.lmp
  cp ${base_dir}/in_fwd.lmp ${base_dir}/${iter_dir}/fwd/in.lmp

  # Setup original lammps data file with topology information

  sed -i 's,'"MYDATA"','"$lmp_data"',g' bwd/in.lmp
  sed -i 's,'"MYDATA"','"$lmp_data"',g' fwd/in.lmp

  # Select shooting point

  shot_point=$(draw_shooting_point)

  if [[ $last_accepted == $ini_trj ]] ; then
    # No accepted trj yet: the current configuration
    # is  extracted from the original trj

    sed -i 's,'"MYTRJ"','"$ini_trj"',g' bwd/in.lmp
    sed -i 's,'"MYTRJ"','"$ini_trj"',g' fwd/in.lmp

    if [[ $shot_point -lt 0 ]] ; then
      let "curr_conf=$ini_conf+$as_step_ini*$shot_point"
    elif [[ $shot_point -gt 0 ]] ; then
      let "curr_conf=$ini_conf+$as_step_ini*$shot_point"
    elif [[ $shot_point == 0 ]] ; then
      let "curr_conf=$ini_conf"
    fi
  else
    # The general case where we opt for the first
    # frame of either the backward or forward trj
    if [[ $shot_point -lt 0 ]] ; then
	curr_conf=$((as_step * shot_point * -1))
	sed -i 's,'"MYTRJ"','"${base_dir}/${last_accepted}/bwd/npt.lammpstrj"',g' bwd/in.lmp
        sed -i 's,'"MYTRJ"','"${base_dir}/${last_accepted}/bwd/npt.lammpstrj"',g' fwd/in.lmp
    elif [[ $shot_point -gt 0 ]] ; then
        curr_conf=$((as_step * shot_point))
        sed -i 's,'"MYTRJ"','"${base_dir}/${last_accepted}/fwd/npt.lammpstrj"',g' bwd/in.lmp
        sed -i 's,'"MYTRJ"','"${base_dir}/${last_accepted}/fwd/npt.lammpstrj"',g' fwd/in.lmp
    elif [[ $shot_point == 0 ]] ; then
        curr_conf=0
        sed -i 's,'"MYTRJ"','"${base_dir}/${last_accepted}/fwd/npt.lammpstrj"',g' bwd/in.lmp
        sed -i 's,'"MYTRJ"','"${base_dir}/${last_accepted}/fwd/npt.lammpstrj"',g' fwd/in.lmp
    fi
  fi

  sed -i 's,'"MYCONF"','"$curr_conf"',g' bwd/in.lmp
  sed -i 's,'"MYCONF"','"$curr_conf"',g' fwd/in.lmp

  sed -i 's,'"MYSTEP"','"$as_step"',g' bwd/in.lmp
  sed -i 's,'"MYSTEP"','"$as_step"',g' fwd/in.lmp

  curr_seed=${RANDOM}

  sed -i 's,'"MYSEED"','"$curr_seed"',g' bwd/in.lmp
  sed -i 's,'"MYSEED"','"$curr_seed"',g' fwd/in.lmp

  # Run forward and backward time propagations

  cd ${base_dir}/${iter_dir}/bwd
  srun lmp -i in.lmp -sf opt

  cd ${base_dir}/${iter_dir}/fwd
  srun lmp -i in.lmp -sf opt

  cd ${base_dir}/${iter_dir}

  # Test if the new trajectory connects the two basins

  connectivity=$(is_connected ${base_dir}/${iter_dir})

  if [[ $connectivity == "True" ]] ; then
    # Accept the trajectory, store the data
    last_accepted=$iter_dir

    cp ${base_dir}/${iter_dir}/bwd/npt.lammpstrj ${base_dir}/AS_trj/bwd_${iter_dir}.lammpstrj
    cp ${base_dir}/${iter_dir}/fwd/npt.lammpstrj ${base_dir}/AS_trj/fwd_${iter_dir}.lammpstrj


    # Store CV values

    #sed '2,2!d' ${base_dir}/${iter_dir}/bwd/colvar >> ${base_dir}/accepted.cv

    acc=$((acc+1))
    tot=$((tot+1))
  else
    rej=$((rej+1))
    tot=$((tot+1))

    rm -f ${base_dir}/${iter_dir}/fwd/npt.lammpstrj
    rm -f ${base_dir}/${iter_dir}/bwd/npt.lammpstrj
  fi
    
  # Update output with statistics

  perc_acc=$(bc <<< "scale=2; 100.*$acc/$tot")

  echo "$a $acc $rej $tot $perc_acc" >> ${base_dir}/statistics.txt
    
  a=$((a+1))

  cd ${base_dir}

done
