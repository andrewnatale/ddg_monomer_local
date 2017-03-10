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

# can be a filename or string 'all'
mutants_input = sys.argv[2]

# load a blacklist that will override the loaded or generated mutant list (for example to avoid duplication)
try:
    blacklist = sys.argv[3]
except IndexError:
    blacklist = None

# make output directory
output_dir = os.path.join(os.getcwd(), 'resfiles')

try:
    os.makedirs(output_dir)
except OSError:
    if os.path.isdir(output_dir):
        print 'ERROR: Output directory \'resfiles\' already exists, rename or remove it and re-run this script.'
        raise

# amino acids
aas = 'ACDEFGHIKLMNPQRSTVWY'

# parse pdb file to get a sequence
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

print 'Found sequence in pdb file:'
print ''.join(seq)

# load list of mutations from a tsv file
# should return a list of tuples with the format:
# (wt aa id, res number, mut aa id)
def load_list(infile, sequence):
    with open(infile, 'r') as mutations:
        targets = mutations.readlines()
    targets = [i.strip().split() for i in targets]
    mut_list = []
    for target in targets:
        if target[0] == sequence[int(target[1])-1]:
            print 'Adding \'%s %s %s\' to the list of mutations' % (target[0],target[1],target[2])
            mut_list.append((target[0],target[1],target[2]))
        else:
           print 'WARNING: Cannot add \'%s %s %s\' because the wt residue does not match the pdb!' % (target[0],target[1],target[2])
    return mut_list

# load a blacklist and edit mutation list before writing resfiles
def load_blacklist(infile, target_list):
    with open(infile, 'r') as mutations:
        nontargets = mutations.readlines()
    nontargets = [i.strip().split() for i in nontargets]
    nontargets = [(i[0],i[1],i[2]) for i in nontargets]
    print 'Applying blacklist to remove unwanted mutations...'
    new_mut_list = [n for n in target_list if n not in nontargets]
    return new_mut_list

# if no list is specified, generate resfiles for every possible mutation
def generate_list(sequence):
    mut_list = []
    for idx,res in enumerate(sequence):
        num = idx + 1
        for aa in aas:
            if res != aa:
                mut_list.append((res, num, aa))
    return mut_list

# parse or generate list
if mutants_input == 'all':
    print 'Generating resfiles for all possible mutations...'
    mutations = generate_list(seq)
else:
    print 'Generating resfiles based on input target mutations...'
    mutations = load_list(mutants_input, seq)

# operate on blacklist if requested
if blacklist:
    mutations = load_blacklist(blacklist, mutations)

# generate resfiles
with open(os.path.join(output_dir, 'resfiles.lst'), 'w') as out_list:
    count = 0
    for mutation in mutations:
        rfilename = '%s%s%s.res' % (mutation[0],mutation[1],mutation[2])
        with open(os.path.join(output_dir, rfilename), 'w') as resfile:
            resfile.write('%s A PIKAA %s' % (mutation[1], mutation[2]))
        out_list.write('%s\n' % str(os.path.join(output_dir, rfilename)))
        count += 1
    print 'Wrote resfiles for %d mutations and listed them in \'resfiles.lst\'' % count

with open(os.path.join(output_dir, 'mutations.lst'), 'w') as out_list:
    for mutation in mutations:
        out_list.write('%s\t%s\t%s\n' % (mutation[0],mutation[1],mutation[2]))
    print 'Wrote considered mutations in blacklist format to \'mutations.lst\''
