# ONAL - ONIOM Analyser
Python script to analyse ONIOM output (log) files from Gaussian.

Written by Gabriel L. S. Rodrigues.


The onal program is a Python script that has as objective the analysis of ONIOM QM/MM calculations output files from Gaussian software, since these files have a large amount of text and information. It requires the instalation of a Python 3 interpreter. Below there are
links to download two options, Python and Anaconda, being the latter a package that includes many scientific focused softwares including a Python interpreter.

https://www.python.org/downloads/

https://www.anaconda.com/download/

## Version 1.0.0
In its current form, version 1.0.0 has the capabilitiy to extract all the geometries of the Quantum Mechanical (QM) treated atoms, including the ones in the Molecular Mechanics (MM) treatment frontier and save them in a single ".qm.all.xyz" file. All the geometries of moving atoms (QM or MM), which are selected by the 0 value in the Gaussian input file are also separated in a single "move.all.xyz" file.

To do the analysis the program needs a Gaussian ONIOM .log file with all calculation geometries and a user made file, exemplified in the info_example.txt in the input_examples folder in the form:
 ```
 C-C_3(PDBName=CA,ResName=HIS,ResNum=152_A)       0   13.20400000   23.94000000   18.51100000 L H-H_ 2313
 C-C_R(PDBName=C,ResName=HIS,ResNum=152_A)        0   14.08000000   25.13400000   18.81300000 L
 C-C_3(PDBName=CB,ResName=HIS,ResNum=152_A)       0   14.05000000   22.65400000   18.42700000 H
 ``` 
 Where L - H-H denotes atoms in the QM/MM frontier region, L atoms in the low level MM region and H the atoms in the high level QM region.
 The info file must not contain any other information and has the format used in the gaussian input.
 
 ### Usage
 
 The usage of the ONAL script is very easy and can be acessed by:
 ``` ./onal.py -h ``` or by ``` ./onal.py --help  ```
 
 The script needs as arguments:
 
 -l or --olog --> Gaussian ONIOM output .log file.
 
 -i or --ifile --> a info/template file.
 
 -o or --ofile --> A optional onal output file name (default = onal.out.txt).
 
 Usage:
 
  ``` onal.py -l oniom_calc.log -i info_file.txt -o output_file.txt ```
  
  ### The input creator module - onal_inp.py
  
  After the onal run, a index (.idx) file is created in the directory with the name **_outputbasename.idx_** which contains the indexes
  of the QM and moving atoms related to the structure of the info file. This file is necessary for a consecutive run of the onal_inp       module. The module selects a geometry from all the ones printed in the .xyz file (by the number on it) and replace the xyz coordinates of the atoms in that geometry with the ones in the info_file initial geometry. All atoms not included in the QM or moving part of the .xyz files do not have any of its coordinates modified.
  
  #### onal_inp usage
  
  ``` onal_inp.py -i info_file.txt -o onion_calc.inp -p prepend_file.txt -a append_file.txt -g geometry_number ```
  
  in which -o specifies the generated Gaussian input file, the  ```-p prepend.txt ``` is a .txt file with all the keywords that will come before the coordinates information, ```-a append.txt ``` is a .txt file with all the keywords that will be printer after the coordinates information and ```-g geometry``` number is the number of the geometry that will be inserted in the input, which can be chosen from the .all.xyz files created by the onal run. 
