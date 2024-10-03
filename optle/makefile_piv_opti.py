import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

def float_or_none(value):
    if value == 'none':
        return None
    try:
        return float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid value: {value}. Must be a float or 'none'.")

parser = argparse.ArgumentParser()
parser.add_argument("--T", type=float)
parser.add_argument("--n_iter", type=int)
parser.add_argument("--dt", type=float)
parser.add_argument("--CV", type=str)
parser.add_argument("--tresh", default='none',type=float_or_none)
parser.add_argument("--gauss_w", type=float_or_none)
args = parser.parse_args()

T = args.T
CV = args.CV
# Directory path
if T==0.65:
    directory = '../mesu_results/trj/' + str(T) + '_trajs/last_trj/'
else:
    directory = '../mesu_results/trj/' + str(T) + '_trajs/'

# List all files in the directory
files = os.listdir(directory)

t = []
p1s = []

dt = args.dt
step = int(dt/0.5)

# Print the list of files
for file in files:
    if 'traj' in file and '.out' in file and 'bck' not in file:
        data = np.loadtxt(directory + file)
        t.append(data[::step, 0])
        p1s.append(data[::step, 3])


t = np.concatenate(t)
p1s = np.concatenate(p1s)


filename = './colvar'

# Write the data into the text file
with open(filename, 'w') as file:
    for i in range(int(len(t)/step)):
        file.write(f"{t[i]} {p1s[i]}\n")

print(f"Data has been written to {filename}")

# Change the input file
filename = './input'

x_max = p1s.max()
x_min = p1s.min()
dt = (t[1]-t[0])

with open(filename, 'r+') as file:
    # Read the file line by line
    lines = file.readlines()
    
    # Move the file cursor to the beginning
    file.seek(0)
    
    # Modify each line
    for line in lines:
        # Split the line into words
        words = line.split()
        line_name = words[0]
        # Check if there are at least two words in the line
        if line_name == 'dt':
            words[1] = str(dt)
             #Join the words back into a line
            modified_line = ' '.join(words) + '\n'
            
            # Write the modified line to the file
            file.write(modified_line)
        elif line_name == 'xmax':
            words[1] = str(x_max)
             #Join the words back into a line
            modified_line = ' '.join(words) + '\n'
            
            # Write the modified line to the file
            file.write(modified_line)  
        elif line_name == 'xmin':
            words[1] = str(x_min)
             #Join the words back into a line
            modified_line = ' '.join(words) + '\n'
            
            # Write the modified line to the file
            file.write(modified_line)
        elif line_name == 'opt_niter':
            words[1] = str(args.n_iter)
             #Join the words back into a line
            modified_line = ' '.join(words) + '\n'
            
            # Write the modified line to the file
            file.write(modified_line)
        elif line_name == 'max_Gaussian_w':
            words[1:4] = [str(args.gauss_w), str(args.gauss_w), str(args.gauss_w)]
             #Join the words back into a line
            modified_line = ' '.join(words) + '\n'
            
            # Write the modified line to the file
            file.write(modified_line)
        else:
            # If there are less than two words, write the original line to the file
            file.write(line)
    
    # Truncate the file to remove any remaining content
    file.truncate()

    # Define the filename
filename = './RESTART'
x_linspace = np.linspace(x_min, x_max, 1000)
# Write the data into the text file
with open(filename, 'w') as file:
    file.write('# x F F/kT gamma mass \n')
    for i in range(1000):
        file.write("{} {} {} 50.0000 1.0000 \n".format(x_linspace[i], 0, 0))

print(f"Data has been written to {filename}")