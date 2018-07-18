# ONIOM Analyser to create inputs

# Imported modules
#import onal
import re, sys, getopt, glob, os

### Functions
# Extract geometry number geom_num from .all.xyz file in a list
def get_geom(xyz_file,catch,geom_num):
    with open(xyz_file, 'r') as inp:
        for line in inp:
            if line.startswith(catch) and line.split()[-1] == str(geom_num):
                new_xyz = []
                for line in inp:
                    try:
                        int(line.strip()[0])
                        new_xyz.append(line.split()[1::])
                    except:
                        break
    return new_xyz

def coord_replace(idx_list,old_xyz,new_xyz):
    temp_coord = [idx[:] for idx in old_xyz]
    for n, idx in enumerate(idx_list):
        for i in (2,3,4):
            temp_coord[idx-1][i] = new_xyz[n][i-2]
    return temp_coord

# Default parameters
inf_file = "template_example.txt"
out_file = "oniom.inp"
move_xyz_file = glob.glob("*.move.all.xyz")[0]
qm_xyz_file = glob.glob("*.qm.all.xyz")[0]
idx_file = glob.glob("*.idx")[0]
prep_file = "prep.txt"
prepend = False
ap_file = "append.txt"
append = False
geom_num = 1

### Getopt Parameters
usage = "Usage: onal_inp.py -i info_file.txt -o output_file.txt -p prepend_file.txt -a append_file.txt -g geometry_number"
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:p:a:g:h', [ 'ifile=', 'ofile=', 'prepend=', 'geometry=' 'append=' 'help' ])
except getopt.GetoptError:
    print(usage)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print(usage)
        sys.exit(2)
    elif opt in ('-i', '--ifile'):
        inf_file = arg
    elif opt in ('-o', '--ofile'):
        out_file = arg
    elif opt in ('-p', '--prepend'):
        prep_file = arg
        prepend = True
    elif opt in ('-a', '--append'):
        ap_file = arg
        append = True
    elif opt in ('-g', '--geometry'):
        geom_num = int(arg)
    else:
        print(usage)
        sys.exit(2)

# Parameters arrays
qm_idx = []
move_idx = []

### Extract indexes from idx file
with open(idx_file,'r') as inp:
    for line in inp:
        if line.startswith("QM"):
            for line in inp:
                try:
                    qm_idx.append(int(line.strip()))
                except ValueError:
                    break
        if line.startswith("Moving"):
            for line in inp:
                try:
                    move_idx.append(int(line.strip()))
                except ValueError:
                    break

### Read info file into memory
with open(inf_file, 'r') as inp:
    old_xyz = []
    #old_xyz.append(" ")
    [ old_xyz.append(line.split()) for line in inp ]

### Get the desired geometry from qm.all.xyz files
new_qm_xyz = get_geom(qm_xyz_file, "QM atoms geometry", geom_num)

### Get the desired geometry from move.all.xyz files (TO LATER IMPLEMENTATION)                    
#new_move_xyz = get_geom(qm_xyz_file,"Moving atoms geometry",geom_num)

# Create the input file and write header and prepend if requested
with open(out_file, 'w') as output:
    if prepend:
        output.write("! Input created by ONIOM Analyser\n")
        with open(prep_file, 'r') as prep:
            [ output.write(line) for line in prep ]
            output.write("\n")
    # Now write the new coordinates
    temp_xyz = coord_replace(qm_idx, old_xyz, new_qm_xyz) # Get new temp xyz
    for line in temp_xyz:
        output.write(" ")
        output.write('   '.join(line))
        output.write("\n")
    # To finish write the append info if requested
    if append:
        output.write("\n")
        with open(ap_file, 'r') as appe:
            [ output.write(line) for line in appe ]

stop = "now"
