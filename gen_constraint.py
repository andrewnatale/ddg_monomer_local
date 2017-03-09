# gen_constraints.py
# parse logfile from minimization output and write out a constaints file
# python 2.x

import sys

infile = sys.argv[1]

with open('mincst.log', 'r') as logfile:
    lines = logfile.readlines()

with open('ca_dist_restraints.cst', 'w') as outfile:
    for line in lines:
        try:
            if line.split()[0] == 'c-alpha':
                outfile.write('AtomPair CA %s CA %s HARMONIC %s %s' % (line.split()[5], line.split()[7], line.split()[9], line.split()[12]))
                outfile.write('\n')
        except IndexError:
            pass