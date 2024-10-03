#!/bin/bash
#SBATCH --job-name=my_fortran_job
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#SBATCH --partition=your_partition
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=10:0:00

# Define an array of arguments
n_iter=5
Ts=(''0.75)
list_iter=('1000000') 
cvs=('e_mesu')
AS=1
dts=('2')
gauss_w=0.01
gauss_h1=1
gauss_h2=1
gauss_h3=0.5
start_time=$(date +%s)

# Iterate over the arguments and run the script
for opt_iter in "${list_iter[@]}"
    do
    for T in "${Ts[@]}"
        do
        for cv in "${cvs[@]}"
            do
            mkdir ../opt_T${T}_${cv}
            for dt in "${dts[@]}"
                do
                    #Plusieurs fichiers makefile, qui servent à générer les fichiers input, PROFILES, etc..., qui devront être uniformisés en un seul
                    if [ "$cv" = "piv" ]; then
                        makefile="makefile_piv_opti.py"
                    elif [ "$cv" = "q6_full" ]; then
                        makefile="makefile_q6_opti.py"
                    elif [ "$cv" = "e_mesu" ]; then
                        makefile="makefile_q6_opti.py"
                    else 
                        makefile="makefile_cut_opti.py"
                    fi
                    echo $makefile
                    python3 $makefile --T $T --dt $dt --CV $cv --AS $AS --gauss_w $gauss_w --gauss_h1 $gauss_h1 --gauss_h2 $gauss_h2 --gauss_h3 $gauss_h3 --n_iter $opt_iter
                    for ((i=0; i<$n_iter; i++))
                    do
                        ./optle 
                        if [ "$AS" = 1 ]; then
                            cp PROFILES ../opt_T${T}_${cv}/as_dt=${dt}_gw=${gauss_w}_gh_${gauss_h1}_${gauss_h2}_${gauss_h3}_cut_${i}_${opt_iter}
                            cp fort.654 ../opt_T${T}_${cv}/as_noise_dt=${dt}_gw=${gauss_w}_gh_${gauss_h1}_${gauss_h2}_${gauss_h3}_cut_${opt_iter}
                        else
                            cp PROFILES ../opt_T${T}_${cv}/dt=${dt}_gw=${gauss_w}_gh_${gauss_h1}_${gauss_h2}_${gauss_h3}_cut_${i}_${opt_iter}
                            cp fort.654 ../opt_T${T}_${cv}/noise_dt=${dt}_gw=${gauss_w}_gh_${gauss_h1}_${gauss_h2}_${gauss_h3}_cut_${opt_iter}
                        fi
                        find -type f -name '*fort.5*' -delete
                    done
                done
            done
        done
    done
done
end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "Elapsed time: $elapsed_time seconds"
