# ONIOM Analyser
# by Gabriel L. S. Rodrigues

# Version
s_version = 1.0

# Imported modules
import re
from itertools import islice

# Functions
### Append to a file ### 
def fowrite(data):
    # data = [FILE, [contents], DIR]    
    out_file = str(data[0])
    contents = data[1]
    #DIR = str(data[2]) # If one wants to include DIR.
    # Enter new DIR and append to the file
    #with cd(DIR):
    with open(out_file,'a') as fo:              
        for line in contents:
            fo.writelines(line)
    return

# Build a file
def buildFILE(dataFILE):
    # dataFILE = [FILE,DIR]
    out_file = str(dataFILE)
    #DIR = str(dataFILE[1])
    # Create new DIR if does not exist    
    #if not os.path.exists(DIR):
    #    os.makedirs(DIR)
    # Create file in DIR
    #with cd(DIR):
    fo = open(out_file, 'w')
    fo.close()
    return

# Regular Expressions (RegEx) patterns
high_pat = re.compile(r'\sH\s')
front_pat = re.compile(r'L\sH-H_')
coord_pat = re.compile(r'Input\sorientation:')

# Text patterns to look up
#high_text = 
#front_text =
input_text = "Input orientation"

# Variables
qm_idx = []
front_idx = []
move_idx = []

# Parameters from prm file
inf_file = "template_example.txt" #sysargv[1]
oniom_file = "out_example.log" #sysargv[3]
move_xyz_file = "oniom.move.all.xyz"
high_xyz_file = "oniom.high.all.xyz" #sysargv[2]
out_file = "onal.out.txt"
xyz_print = 2 # 0 to print high level and moving atoms, 1 to print only moving atoms and 2 to print only high level atoms

# Open the information file with atom description and get the high level and frontier atoms.
with open(inf_file, 'r') as foo:
    index = 1
    for line in foo:
        if int(line.split()[1]) == 0:
            move_idx.append(index)
        if not re.search(high_pat, line) and not re.search(front_pat, line): # Add index counter for lines without match
            index += 1
            continue
        elif re.search(high_pat, line): # High level calculation atom indexes
            qm_idx.append(index)
            index += 1
        elif re.search(front_pat, line): # Frontier QM/MM atom indexes
            front_idx.append(index) # If it is necessary to separate the frontier atoms later
            qm_idx.append(index)
            index += 1
    # Defining the number of atoms: total, only high level, frontier, all high level and moving
    numb_atoms = index - 1
    numb_qm = len(qm_idx)
    numb_front = len(front_idx)
    numb_high = numb_qm - numb_front
    numb_move = len(move_idx)
    #print("HIGH = \n", qm_idx, "\nFront = \n", front_idx, "Move = ", move_idx)

# Create the output files from scratch and start to write on it.
# General output file
buildFILE(out_file)
text = "#####  Starting ONIOM Analyser Version {:.2f}  #####\
\nMade by Gabriel L. S. Rodrigues\n\
\nTotal number of atoms    = {:6d} \nTotal number of QM atoms = {:6d}\
\nNumber of frontier atoms = {:6d}".format(s_version,numb_atoms,numb_qm,numb_front)
fowrite([out_file,text])
# Moving atoms xyz file
buildFILE(move_xyz_file)
# High level atoms xyz file
buildFILE(high_xyz_file)
    
# Open the ONIOM calculation file and extract:
# the coordinates of moving atoms, high level atoms and total number of atoms.
with open(oniom_file, 'r') as foo:
    index = 0
    ncoord = 0
    count = 0
    start = False
    for line_numb, line in enumerate(foo, 1): 
        index = line_numb - count # Index corresponding to the atom number in hatoms and fatoms
        ### Starting the conditionals
        # Find the string Input orientation
        if re.search(coord_pat, line):
            start = True
            ncoord += 1
            count = line_numb + 4
            current_coord = []
            # Write the number of atoms and geometry number in xyz files
            text_high = str(numb_qm) + "\nQM atoms geometry {:6d}\n".format(ncoord)
            text_move = str(numb_move) + "\nMoving atoms geometry {:6d}\n".format(ncoord)
            fowrite([high_xyz_file,text_high])
            fowrite([move_xyz_file,text_move])
            print("Writing geometry {:d}".format(ncoord))
            continue
        # Check if it is in start coordinates mode,
        # which starts with coord_pat string and ends when there are no integers in the start of the line
        elif not start:
            continue
        elif index < 1: # Jump to lines with the coordinates.
            continue
        ## Starting with the coordinates writing
        # Finding the lines with the desired atoms.
        if index <= numb_atoms:
        #elif (index in (move_idx or qm_idx or front_idx)) and start:
            sline = line.split()
            del sline[0]
            del sline[1]
            new_line = '     '.join(sline)+"\n"
            current_coord.append(new_line)
        # Check if list of atoms coordinates finished, if so, sets start to False.
        try: 
            int(line.split()[0])
        except ValueError: # When all coordinates from given geometry ends
            # Write to QM file.
            text_high = [current_coord[i-1] for i in qm_idx]
            text_high.append(">\n")
            fowrite([high_xyz_file,text_high])
            # Write to moving atoms file.
            text_move = [current_coord[i-1] for i in move_idx]
            text_move.append(">\n")
            fowrite([move_xyz_file,text_move])
            start = False