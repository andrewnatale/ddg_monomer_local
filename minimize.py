# minimization.py
# python 2.x script to run rosetta's minimize_with_cst application on an
# input pdb file in preparation for running the ddg_monomer application

import socket
import sys
import os
import subprocess

# make this convert to full path for safety
input_pdb_file = sys.argv[1]
# paramsfiles?
input_params_file = 'test'

# script default settings
rosetta_bindir = "/some/dir"
rosetta_appname = "minimize_with_cst"
platform_tag = "linuxgccrelease"
rosetta_db_dir = "/some/otherdir/database"
output_dir = os.getcwd()

# TODO: read in above settings from a file instead of hardcoding
def get_settings():
    pass

# what command line should look like from rosetta documentation:
"""
/path/to/minimize_with_cst.linuxgccrelease
-in:file:l lst  -in:file:fullatom -ignore_unrecognized_res
-fa_max_dis 9.0 -database /path/to/rosetta/main/database/
-ddg::harmonic_ca_tether 0.5 -score:weights standard -ddg::constraint_weight 1.0
-ddg::out_pdb_prefix min_cst_0.5 -ddg::sc_min_only false
-score:patch rosetta/main/database/scoring/weights/score12.wts_patch > mincst.log
"""

# generate rosetta command line
rosetta_cmd = [
os.path.join(rosetta_bindir,'%s.%s' % (rosetta_appname, platform_tag)),
'-in:file', input_pdb_file,
'-database', rosetta_db_dir,
'-in:file:fullatom', '-ignore_unrecognized_res',
'-fa_max_dis', '9.0', '-ddg::harmonic_ca_tether', '0.5',
'-ddg::constraint_weight', '1.0',
'-ddg::out_pdb_prefix', 'min_cst_0.5',
'-ddg::sc_min_only', 'false'
]

if input_params_file:
    rosetta_cmd.append('-extra_res_fa')
    rosetta_cmd.append(input_params_file)

print rosetta_cmd

os.chdir(output_dir)
with open('mincst.log', 'w') as logfile:
    logfile.write("Python: %s\n" % sys.version)
    logfile.write("Host: %s\n" % socket.gethostname())

with open('mincst.log', 'a+') as logfile:
    process = subprocess.Popen(rosetta_cmd, \
                               stdout=logfile, \
                               stderr=subprocess.STDOUT, \
                               close_fds = True)
    returncode = process.wait()
