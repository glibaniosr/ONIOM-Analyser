# ONIOM Analyser
# by Gabriel L. S. Rodrigues
# July 2018

# Version
s_version = "1.0.0"

# Imported modules
import re, sys, getopt, glob, os

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

# Default parameters
oniom_file = "out_example.log"
inf_file = "template_example.txt"
out_file = "onal.out.txt"
move_xyz_file = "onal.move.all.xyz"
qm_xyz_file = "onal.qm.all.xyz"
xyz_print = 2 # 0 to print QM and moving atoms, 1 to print only moving atoms and 2 to print only QM atoms

# Getopt Parameters
usage = "Usage: onal.py -l oniom_calc.log -i info_file.txt -o output_file.txt"
try:
    opts, args = getopt.getopt(sys.argv[1:], 'l:i:o:hv', ['olog=', 'ifile=', 'ofile=', 'help', 'version'])
except getopt.GetoptError:
    print(usage)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print(usage)
        sys.exit(2)
    if opt in ('-v', '--version'):
        print("ONIOM Analyser Version {:s}".format(s_version))
        sys.exit(2)
    elif opt in ('-l', '--olog'):
        oniom_file = arg
    elif opt in ('-i', '--ifile'):
        inf_file = arg
    elif opt in ('-o', '--ofile'):
        out_file = arg
    else:
        print(usage)
        sys.exit(2)

# Auxiliar files
out_basename,ext = os.path.splitext(out_file)
idx_file = out_basename+".idx"

# RegEx patterns
high_pat = re.compile(r'\sH\s')
front_pat = re.compile(r'L\sH-H_')
coord_pat = re.compile(r'Input\sorientation:')

# Important data arrays
qm_idx = [] # Stores QM atom indexes
front_idx = [] # Stores frontier atom indexes
move_idx = [] # Stores moving atoms indexes

# Open the information file with atom description and get the QM only and frontier atoms.
with open(inf_file, 'r') as foo:
    index = 1
    for line in foo:
        if int(line.split()[1]) == 0:
            move_idx.append(index)
        if not re.search(high_pat, line) and not re.search(front_pat, line): # Add index counter for lines without match
            index += 1
            continue
        elif re.search(high_pat, line): # QM calculation atom indexes
            qm_idx.append(index)
            index += 1
        elif re.search(front_pat, line): # Frontier QM/MM atom indexes
            front_idx.append(index) # If it is necessary to separate the frontier atoms later
            qm_idx.append(index)
            index += 1
    # Defining the number of atoms: total, only QM level, frontier, all QM and moving
    numb_atoms = index - 1
    numb_qm = len(qm_idx)
    numb_front = len(front_idx)
    numb_high = numb_qm - numb_front
    numb_move = len(move_idx)
    #print("HIGH = \n", qm_idx, "\nFront = \n", front_idx, "Move = ", move_idx)

# Create the output files from scratch and start to write on it.
# General output file
buildFILE(out_file)
text = "#####  Starting ONIOM Analyser Version {:s}  #####\
\nMade by Gabriel L. S. Rodrigues\n\
\nTotal number of atoms    = {:6d} \nTotal number of QM atoms = {:6d}\
\nNumber of frontier atoms = {:6d}".format(s_version,numb_atoms,numb_qm,numb_front)
fowrite([out_file,text])
# Moving atoms xyz file
buildFILE(move_xyz_file)
# QM atoms xyz file
buildFILE(qm_xyz_file)
# Indexes file
buildFILE(idx_file)
    
### Write the indexes to the index file:
# QM part
with open(idx_file,'a') as output:
    output.write("QM atoms index\n")
    [ output.write(str(idx)+"\n") for idx in qm_idx ]
    output.write(">\n")
# Moving part
with open(idx_file,'a') as output:
    output.write("Moving atoms index\n")
    [ output.write(str(idx)+"\n") for idx in move_idx ]
    output.write(">\n")
    
# Open the ONIOM calculation file and extract:
# the coordinates of moving atoms, QM atoms and total number of atoms.
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
            fowrite([qm_xyz_file,text_high])
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
            fowrite([qm_xyz_file,text_high])
            # Write to moving atoms file.
            text_move = [current_coord[i-1] for i in move_idx]
            text_move.append(">\n")
            fowrite([move_xyz_file,text_move])
            start = False