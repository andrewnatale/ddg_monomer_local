# gen_mutfiles.py
# a script to generate mutation specification files for running rosetta's
# ddg_monomer application

import os
import sys
from Bio.PDB import *

# input
pdb_file = sys.argv[1]
try:
    mutant_list = sys.argv[2]
except IndexError:
    mutant_list = 'all'
# output directory
output_dir = os.getcwd()
# how granular should the lists be
mutations_per_list = 2

# parse pdb file to get sequence
p = PDBParser(PERMISSIVE=1)
structure = p.get_structure(pdb_file, pdb_file)


# TODO: load list of mutations (not sure what format yet)
# should return a list of tuples with the format:
# (wt aa id, res number, mut aa id)
def load_list(filename):
    mut_list = dummy_muts
    return mut_list

# if no list is specified, generate mutfiles for every possible mutation
def generate_list():
    pass

dummy_muts = [
('A', 105, 'D'),
('Q', 250, 'F'),
('G', 20, 'E'),
('T', 106, 'A')
]

total_mutations
