# minimize.py
# python 2.x script to run rosetta's minimize_with_cst application on an
# input pdb file in preparation for running the ddg_monomer application

import socket
import sys
import os
import subprocess

# we have to input a list, because apparently single file input is broken in minimize_with_cst
input_pdb_list = os.path.abspath(sys.argv[1])
# paramsfiles?
input_params_file = None

# script default settings
rosetta_bindir = "/opt/rosetta/rosetta_current/source/bin"
rosetta_appname = "minimize_with_cst"
platform_tag = "linuxgccrelease"
rosetta_db_dir = "/opt/rosetta/rosetta_current/database"
output_dir = os.getcwd()

# TODO: read in above settings from a file instead of hardcoding
def get_settings():
    pass

# what the command line should look like from the rosetta documentation:
"""
/path/to/minimize_with_cst.linuxgccrelease
-in:file:l lst  -in:file:fullatom -ignore_unrecognized_res
-fa_max_dis 9.0 -database /path/to/rosetta/main/database/
-ddg::harmonic_ca_tether 0.5 -score:weights standard -ddg::constraint_weight 1.0
-ddg::out_pdb_prefix min_cst_0.5 -ddg::sc_min_only false
-score:patch rosetta/main/database/scoring/weights/score12.wts_patch > mincst.log
"""

# generate rosetta command line args
rosetta_cmd = [
os.path.join(rosetta_bindir,'%s.default.%s' % (rosetta_appname, platform_tag)),
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
if input_params_file:
    rosetta_cmd.append('-extra_res_fa')
    rosetta_cmd.append(input_params_file)

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
