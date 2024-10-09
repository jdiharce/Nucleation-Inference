#!/bin/bash
# Define the number of random numbers to generate
num_random_numbers=100

# Declare an associative array to store unique random numbers
declare -A random_numbers

# Loop to generate random numbers
while [ ${#random_numbers[@]} -lt $num_random_numbers ]
    do
        # Generate a random number between 1 and 100
        random_number=$RANDOM
        
        # Add the random number to the associative array if it doesn't already exist
        random_numbers[$random_number]=$random_number
    done

for number in "${random_numbers[@]}"
    do
	echo ${number}
        sed s/XXX/${number}/ input_gen.lmp > input${number}.lmp
	sed s/XXX/${number}/ lmp_gen.sh > lmp${number}.sh
        sbatch lmp${number}.sh
	rm lmp${number}.sh
    done
