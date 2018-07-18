# ONIOM Analyser to create inputs

# Imported modules
import onal
import re, sys, getopt, glob, os

# Default parameters
inf_file = "template_example.txt"
out_file = "oniom.inp"
move_xyz_file = glob.glob(".move.all.xyz")
high_xyz_file = glob.glob(".qm.all.xyz")
xyz_print = 2 # 0 to print QM and moving atoms, 1 to print only moving atoms and 2 to print only QM atoms

# Getopt Parameters
usage = "Usage: onal_inp.py -i info_file.txt -o output_file.txt -p prepend_file.txt -a append_file.txt"
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:p:a:h', [ 'ifile=', 'ofile=', 'prepend=', 'append=' 'help' ])
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
        out_file = arg
    elif opt in ('-a', '--append'):
        out_file = arg
    else:
        print(usage)
        sys.exit(2)

