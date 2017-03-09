# gen_mutfiles.py
# a script to generate mutation specification files for running rosetta's
# ddg_monomer application
# depends on Biopython's PDB parsing module

import os
import sys
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Polypeptide import three_to_one
from Bio.PDB.Polypeptide import is_aa

# input - the pdb file should probably be a rosetta generated file for fewer unpleasant surprises
pdb_file = sys.argv[1]
try:
    mutants_input = sys.argv[2]
except IndexError:
    mutants_input = 'all'
# output directory
output_dir = os.getcwd()
# how granular should the lists be?
mutations_per_list = 10

# amino acids
aas = 'ACDEFGHIKLMNPQRSTVWY'

# parse pdb file to get sequence
p = PDBParser(PERMISSIVE=1)
structure = p.get_structure(pdb_file, pdb_file)
for model in structure:
    for chain in model:
        # only consider chain A
        if chain.get_id() == 'A':
            seq = []
            for residue in chain:
                if is_aa(residue.get_resname(), standard=True):
                    seq.append(three_to_one(residue.get_resname()))
                else:
                    print 'WARNING: Nonstandard residue %s found in chain A.' % residue.get_resname()
                    print 'This residue will not be added to the sequence, make sure your pdb is ok.'
        else:
            print 'WARNING: Found chain with id other than \'A\'.'
            print 'If this chain is a protein, you will have problems with ddg_monomer later on (ligands are ok if you\'ve accounted for them).'

# TODO: load list of mutations (not sure what format yet)
# should return a list of tuples with the format:
# (wt aa id, res number, mut aa id)
def load_list(list_file, sequence):
    mut_list = dummy_muts
    return mut_list

# if no list is specified, generate mutfiles for every possible mutation
def generate_list(sequence):
    mut_list = []
    for idx,res in enumerate(sequence):
        num = idx + 1
        for aa in aas:
            if res != aa:
                mut_list.append((res, num, aa))
    return mut_list

dummy_muts = [
('A', 105, 'D'),
('Q', 250, 'F'),
('G', 20, 'E'),
('T', 106, 'A')
]

if mutants_input == 'all':
    targets = generate_list(seq)
else:
    targets = load_list(mutants_input, seq)

# generate mutfiles
