import pyscal.core as pc
import os
import pyscal.traj_process as ptp
import pyscal.core as pc
import os
import pyscal.traj_process as ptp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--T", type=float)
args = parser.parse_args()

T =args.T
os.chdir('/store/diharcej/LJ/{}_trj/last_trj/'.format(T))
#os.mkdir('./q6_colvar')


def doQ6(input_file, cutoff_q6 = 0.25, format="lammps-dump"):
    output_file=input_file.replace(".lammpstrj.snap.","_").replace(".dat","_BIS.lammpstrj")
    sys = pc.System()
    sys.read_inputfile(input_file, format=format)
    sys.find_neighbors(method='cutoff',cutoff='adaptive',padding=1.5)
    sys.calculate_q(6,averaged=True)
    def condition(atom):
        return atom.get_q(6,averaged=True) > cutoff_q6
    sys.cluster_atoms(condition)
    atoms = sys.atoms
    clusters = [atom.cluster for atom in atoms if atom.cluster != -1]
    unique_clusters, counts = np.unique(clusters, return_counts=True)
    sys.to_file(output_file, format='lammps-dump',customkeys = ['aq6','cluster'])
    return unique_clusters, counts


files = glob.glob("*trj") 
for input_file in files:
    if 'snap' not in input_file and 'BIS' not in input_file:
        print(input_file)
        files = ptp.split_trajectory(input_file)
        q6clusters = []
        for file in files:
            cluster = doQ6(file)[1]
            if cluster.size==0:
                cluster=0
            else:
                cluster=cluster[0]
            q6clusters.append(cluster)
        filename = './q6_colvar/' + input_file.split('.')[0] + '_q6.out'
        count=1
        # Open the file in write mode
        with open(filename, 'w') as file:
            # Iterate through the list and write each item to the file
            file.write('#! Frames q6 \n')
            for item in q6clusters:
                file.write(str(count) + ' ' + str(item) + '\n')
                count += 1
files = glob.glob("*trj")
for file in files:
    if 'snap' in file or 'BIS' in file:
         os.remove(file)
