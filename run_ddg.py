# run_ddg.py
# script to run rosetta's ddg_monomer application
# takes input from preminimzation scripts and files defining target mutations as input

'-in:file:fullatom', '-ignore_unrecognized_res', '-fa_max_dis', '9.0',
'-ddg::dump_pdbs' ,'true', '-ddg::suppress_checkpointing' ,'true',
'-ddg:weight_file' ,'soft_rep_design' ,'-ddg::iterations' ,str(number_of_structural_pairs),
'-ddg::local_opt_only' ,'false' ,'-ddg::min_cst' ,'true',
'-ddg::mean' ,'false' ,'-ddg::min', 'true',
'-ddg::sc_min_only' ,'false',
'-ddg::ramp_repulsive', 'true'
