#!/bin/bash

#directory to search for files
directory="./0.66_trj"

lines_to_extract=$((4009 * 5000))

# Loop through each file in the directory containing 'test' in its name
for file in "$directory"/*; do
    # Check if the file contains 'test' in its name and is a regular file
    if [[ "$file" == *dump* && -f "$file" ]]; then
        # Extract the filename without the directory path
        filename=$(basename "$file")
	echo $filename
        
        # Create the output filename by appending '_last100' to the original filename
        output_file="$directory/last_trj/last_$filename"
        
        # Extract the last 100 lines and save them to the new file
        tail -n $lines_to_extract "$file" > "$output_file"
    fi
done
