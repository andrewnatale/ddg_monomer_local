# minimize.py
# python 2.x
"""
This script runs rosetta's minimize_with_cst application on an
input PDB file in preparation for running the ddg_monomer application.

It generates a minimized PDB file, a log, and a text file containing the c-alpha
constraints information for ddg_monomer.

Arguments:

1st - text file containing the path to the input pdb (minimize_with_cst reqires input in list format)

2nd (optional) - directory to write output files, created if it does not exist (defaults to 'minimization' in the cwd)

Requires having a 'rosetta.settings' file in the current working directory
to know where to look for rosetta binaries and database files.

The rosetta documentation for ddg_monomer specifies these flags for the minimization step:

/path/to/minimize_with_cst.linuxgccrelease
-in:file:l lst  -in:file:fullatom -ignore_unrecognized_res
-fa_max_dis 9.0 -database /path/to/rosetta/main/database/
-ddg::harmonic_ca_tether 0.5 -score:weights standard -ddg::constraint_weight 1.0
-ddg::out_pdb_prefix min_cst_0.5 -ddg::sc_min_only false
-score:patch rosetta/main/database/scoring/weights/score12.wts_patch > mincst.log
"""

import socket
import sys
import os
import subprocess

# we have to input a list, because apparently single file input is unsupported in minimize_with_cst
input_pdb_list = os.path.abspath(sys.argv[1])
# output path for pdbs and logs (created)
try:
    output_dir = os.path.abspath(sys.argv[2])
except IndexError:
    output_dir = os.path.join(os.getcwd(), 'minimization')
# paramsfiles?
#input_params_file = None

rosetta_appname = "minimize_with_cst"

# load settings file (must be in cwd)
with open('rosetta.settings', 'r') as settingsfile:
    s = settingsfile.readlines()
s = [i.strip() for i in s]
for line in s:
    if line.startswith('#') or line == '':
        continue
    else:
        elem = line.split()
        if elem[0] == 'rosetta_bindir':
            rosetta_bindir = elem[1]
        elif elem[0] == 'rosetta_db_dir':
            rosetta_db_dir = elem[1]
        elif elem[0] == 'platform_tag':
            platform_tag = elem[1]
        elif elem[0] == 'bin_tag':
            bin_tag = elem[1]
        elif elem[0] == 'processes':
            pass
        else:
            print '\nWARNING: Unrecognized setting: %s\n' % line

try:
    os.makedirs(output_dir)
except OSError:
    if not os.path.isdir(output_dir):
        raise

def minimize():
    # generate rosetta command line args
    rosetta_cmd = [
    os.path.join(rosetta_bindir,'%s.%s.%s' % (rosetta_appname, bin_tag, platform_tag)),
    '-in:file:l', input_pdb_list,
    '-database', rosetta_db_dir,
    '-in:file:fullatom', '-ignore_unrecognized_res',
    '-fa_max_dis', '9.0', '-ddg::harmonic_ca_tether', '0.5',
    '-ddg::constraint_weight', '1.0',
    '-ddg::out_pdb_prefix', 'min_cst_0.5',
    '-ddg::sc_min_only', 'false',
    '-in:auto_setup_metals',
    '-score:patch', os.path.join(rosetta_db_dir, 'scoring/weights/score12.wts_patch')
    ]

    # add paramsfile options if needed !!UNTESTED!!
    # if input_params_file:
    #     rosetta_cmd.append('-extra_res_fa')
    #     rosetta_cmd.append(input_params_file)

    # write some system info to the logfile
    os.chdir(output_dir)
    with open('mincst.log', 'w') as logfile:
        logfile.write("Python: %s\n" % sys.version)
        logfile.write("Host: %s\n" % socket.gethostname())
        logfile.write(' '.join(rosetta_cmd))
        logfile.write('\n')

    # call rosetta and write output to log
    with open('mincst.log', 'a+') as logfile:
        process = subprocess.Popen(rosetta_cmd, \
                                   stdout=logfile, \
                                   stderr=subprocess.STDOUT, \
                                   close_fds = True)
        returncode = process.wait()

def write_constraints():
    os.chdir(output_dir)

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

minimize()
write_constraints()
