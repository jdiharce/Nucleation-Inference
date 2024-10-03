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
parser.add_argument("--AS", type=int) # 0 to take brute force data, 1 to take AS data
parser.add_argument("--tresh", default='none',type=float_or_none)
parser.add_argument("--gauss_w", type=float_or_none)
parser.add_argument("--gauss_h1", type=float)
parser.add_argument("--gauss_h2", type=float)
parser.add_argument("--gauss_h3", type=float)
args = parser.parse_args()



def get_index(data, treshold, position, below_or_above):
    # Iterate through the list in reverse order
    if position=='first':
        for i, value in enumerate(data):
            if below_or_above=='above':
                if value > treshold:
                    return i
            if below_or_above=='below':
                if value < treshold:
                    return i
        return -1
    if position=='last':
        for i in range(len(data) - 1, -1, -1):
            if below_or_above=='above':
                if data[i] > treshold:
                    return i
            if below_or_above=='below':
                if data[i] < treshold:
                    return i
        return -1  # Return -1 if no element is above the given value

T = args.T
CV = args.CV
AS = args.AS
# Directory pat
if AS:
    if CV=='q6_full':
        directory = '../mesu_results/AS_{}/q6_colvar/'.format(str(T).split('.')[0] + str(T).split('.')[1])
    if CV=='e_mesu':
        directory = '../mesu_results/AS_{}/e_colvar/'.format(str(T).split('.')[0] + str(T).split('.')[1])
else:
    if CV=='q6_full':
        directory = '../mesu_results/trj/' + str(T) + '_trajs/q6_colvar/'
    if CV=='e_mesu':
        directory = '../mesu_results/trj/' + str(T) + '_trajs/e_colvar/'

# List all files in the directory
files = os.listdir(directory)

t = []
cvs = []

if CV=='q6_full':
    if T==0.75:
        tresh = 500
    else:
        tresh = 80
if CV=='e_mesu':
    if T==0.75:
        tresh_cry = -7.15
        tresh_liq = -6.85
    else:
        tresh = -7.5

dt = args.dt
step = int(dt/0.5)

# Print the list of files

bwd_colvar = []
fwd_colvar = []
for file in files:
    if AS:
        if T==0.75:
            if 'q6' in CV:
                if int(((file.split('/')[-1]).split('.')[0]).split('_')[-2]) > 600:
                    if 'bwd' in file:
                        data = np.loadtxt(directory + file)
                        if CV=='q6_full':
                            cv = data[::step, 1]
                            bwd_colvar.append(cv[::-1])
                        if CV=='e_mesu':
                            cv = data[::step]
                            bwd_colvar.append(cv[::-1])
                            
                    if 'fwd' in file:
                        data = np.loadtxt(directory + file)
                        if CV=='q6_full':
                            cv = data[::step, 1]
                            fwd_colvar.append(cv[::])
                        if CV=='e_mesu':
                            cv = data[::step]
                            fwd_colvar.append(cv[::])
            else:
                if int(((file.split('/')[-1]).split('.')[0]).split('_')[-1]) > 600:
                    if 'bwd' in file:
                        data = np.loadtxt(directory + file)
                        if CV=='q6_full':
                            cv = data[::step, 1]
                            bwd_colvar.append(cv[::-1])
                        if CV=='e_mesu':
                            cv = data[::step]
                            bwd_colvar.append(cv[::-1])
                            
                    if 'fwd' in file:
                        data = np.loadtxt(directory + file)
                        if CV=='q6_full':
                            cv = data[::step, 1]
                            fwd_colvar.append(cv[::])
                        if CV=='e_mesu':
                            cv = data[::step]
                            fwd_colvar.append(cv[::])
        else:
            if 'bwd' in file:
                data = np.loadtxt(directory + file)
                if CV=='q6_full':
                    cv = data[::step, 1]
                    bwd_colvar.append(cv[::-1])
                if CV=='e_mesu':
                    cv = data[::step]
                    bwd_colvar.append(cv[::-1])
                    
            if 'fwd' in file:
                data = np.loadtxt(directory + file)
                if CV=='q6_full':
                    cv = data[::step, 1]
                    fwd_colvar.append(cv[::])
                if CV=='e_mesu':
                    cv = data[::step]
                    fwd_colvar.append(cv[::])
                
    if not AS:
        data = np.loadtxt(directory + file)
        if CV=='q6_full':
            t.append(data[::step, 0])
            cvs.append(data[::step, 1])
        if CV=='e_mesu':
            cv = data[::step]
            cvs.append(cv)
            t.append(np.array([0.5*i*step for i in range(len(cv))]))

if not AS:
    idxs_1 = np.zeros(len(t))
    idxs_2 = np.zeros(len(t))
    for i in range(len(t)):
        #tentative de réaliser la même opération que pour les colvars de Line et Karen i.e. récupérer le debut de la transition uniquement 
        #et construire un colvar où la transition représente 10% du colvar mais ne marchait pas à cause des quelques bugs lors du calcul de 
        #Q6. À uniformiser après avoir régler les bugs.
        l = cvs[i]
        if CV=='q6_full':
            idxs_1[i] = get_index(l, 10, 'last', 'below')
            idxs_2[i] = get_index(l, tresh, 'first', 'above')
        if CV=='e_mesu':
            idxs_1[i] = get_index(l, -7.28, 'last', 'above')
            idxs_2[i] = get_index(l, tresh, 'first', 'below')
    t_cut = []
    cv_cut = []

    for i in range(len(t)):
        if idxs_2[i] != -1:
            idx_1 = int(idxs_1[i])
            idx_2 = int(idxs_2[i])
            shift = (idx_2 - idx_1)*9
            print(idx_1, shift, idx_2)
            #print(idx_1, idx_2)
            #print((idx_2 - idx_1))
            #if shift > idx_1:
            #   t_cut.append(t[i][0:idx_2] - t[i][(0):idx_2].min())
            #  q6_cut.append(q6[i][(0):idx_2])
            #else:
            #   t_cut.append(t[i][(idx_1 - shift):idx_2] - t[i][(idx_1 - shift):idx_2].min())
            #  q6_cut.append(q6[i][(idx_1 - shift):idx_2])
            if CV=='q6_full':
                t_cut.append(t[i][:idx_2] - t[i][:idx_2].min())
                cv_cut.append(cvs[i][:idx_2])
            if CV=='e_mesu':
                if shift > idx_1:
                    t_cut.append(t[i][0:idx_2] - t[i][(0):idx_2].min())
                    cv_cut.append(cvs[i][0:idx_2])
                else:
                    t_cut.append(t[i][(idx_1 - shift):idx_2] - t[i][(idx_1 - shift):idx_2].min())
                    cv_cut.append(cvs[i][(idx_1 - shift):idx_2])
            


    t = np.concatenate(t_cut)
    cvs = np.concatenate(cv_cut)

if AS:
    cvs = []
    t = []
    for i in range(len(bwd_colvar)):
        if CV=='e_mesu' and T==0.75:
            idx_cry = get_index(fwd_colvar[i], tresh_cry, 'first', 'below')
            idx_liq =  get_index(bwd_colvar[i], tresh_liq, 'last', 'below')
            col = np.concatenate([bwd_colvar[i][idx_liq:], fwd_colvar[i][:idx_cry]])
            cvs.append(col)
            t.append(np.array([i*0.5*step for i in range(len(col))]))
        elif CV=='e_mesu' and T!=0.75:
            idx = get_index(fwd_colvar[i], tresh, 'first', 'below')
            col = np.concatenate([bwd_colvar[i], fwd_colvar[i][:idx]])
            cvs.append(col)
            t.append(np.array([i*0.5*step for i in range(len(col))]))
        elif CV=='q6_full':
            idx = get_index(fwd_colvar[i], tresh, 'first', 'above')
            col = np.concatenate([bwd_colvar[i], fwd_colvar[i][:idx]])
            cvs.append(np.concatenate([bwd_colvar[i], fwd_colvar[i][:idx]]))
            t.append(np.array([i*0.5*step for i in range(len(col))]))
    t = np.concatenate(t)
    cvs = np.concatenate(cvs)


filename = './colvar'

# Write the data into the text file
with open(filename, 'w') as file:
    for i in range(int(len(t)/step)):
        file.write(f"{t[i]} {cvs[i]}\n")

print(f"Data has been written to {filename}")

# Change the input file
filename = './input'

print(cvs.min())
x_max = cvs.max()
x_min = cvs.min()
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
        elif line_name == 'max_Gaussian_h':
            words[1:4] = [str(args.gauss_h1), str(args.gauss_h2), str(args.gauss_h3)]
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