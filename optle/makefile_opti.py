import os
import numpy as np
import matplotlib.pyplot as plt
import argparse



parser = argparse.ArgumentParser()

def float_or_none(value):
    if value == 'none':
        return None
    try:
        return float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid value: {value}. Must be a float or 'none'.")
parser.add_argument("--T", type=float)
parser.add_argument("--n_iter", type=int)
parser.add_argument("--dt", type=float)
parser.add_argument("--CV", type=str)
parser.add_argument("--tresh", default='none',type=float_or_none)
parser.add_argument("--gauss_w", type=float_or_none)
args = parser.parse_args()

T = args.T
# Directory path
directory = '../../Documents/binarylj-md-T' + str(T) + '/T' + str(T) + '/'

# List all files in the directory
files = os.listdir(directory)

t = []
s = []
e = []
aq6 = []
q6 = []

dt = args.dt
step = int(dt/0.5)

# Print the list of files
for file in files:
    data = np.loadtxt(directory + file + '/colvar.out')
    t.append(data[2000::step, 0])
    s.append(data[2000::step, 1])
    e.append(data[2000::step, 2])
    aq6.append(data[2000::step, 4])
    q6.append(data[2000::step, 5])

t = np.concatenate(t)
s = np.concatenate(s)
e = np.concatenate(e)
aq6 = np.concatenate(aq6)
q6 = np.concatenate(q6)

tresh_s = -5
tresh_e = -8
tresh_aq6 = 3000
tresh_q6 = 0.375

dict_cv = {}
dict_cv['s'] = s
dict_cv['e'] = e
dict_cv['aq6'] = aq6
dict_cv['q6'] = q6

dict_tresh = {}
dict_tresh['s'] = tresh_s
dict_tresh['e'] = tresh_e
dict_tresh['aq6'] = tresh_aq6
dict_tresh['q6'] = tresh_q6

if args.tresh is not None:
    tresh = args.tresh
else:
    tresh = dict_tresh[args.CV]
CV = dict_cv[args.CV]
# Define the filename
filename = './colvar'

with open(filename, 'w') as file:
    for i in range(int(len(t)/step)):
        if 's' in args.CV or 'e' in args.CV:
            if CV[i] > tresh:
                file.write("%s %s\n" % (t[i], CV[i]))
        else:
            if CV[i] < tresh:
                file.write("%s %s\n" % (t[i], CV[i]))

print(f"Data has been written to {filename}")

# Change the input file
filename = './input'

if 's' in args.CV or 'e' in args.CV:
    x_max = CV[CV>tresh].max()
    x_min = CV[CV>tresh].min()
else:
    x_max = CV[CV<tresh].max()
    x_min = CV[CV<tresh].min()
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