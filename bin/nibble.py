#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

from argparse import ArgumentParser

from multiprocessing import cpu_count
from pdb import set_trace

from nibble import config
reload(config)
from nibble import spm
reload(spm)
from nibble import util
reload(util)

try:
    from joblib import Parallel, delayed
    use_joblib = True
except ImportError:
    use_joblib = False

def parse_args():

    ap = ArgumentParser(description='nibble [options]')
    
    #add arguments
    ap.add_argument('--cfg', nargs='+', default=[])
    ap.add_argument('--study', nargs=1, default='')
    ap.add_argument('--run', default=False, action='store_true')
    ap.add_argument('--nogen', default=True, dest='gen', action='store_false')
    ncpu_choice = [-1]
    ncpu_choice.extend(range(1, cpu_count() + 1))
    ap.add_argument('--ncpu', default=2, type=int, choices=ncpu_choice)
    return ap.parse_args()
    
def run_subject(subj):
    subj.run()
    
if __name__ == '__main__':

    arg = parse_args()

    #starting with config
    if len(arg.cfg) > 0:
        cfg = config.Configurator(arg.cfg, verbose=1)
        study_path = cfg.save()
    elif arg.study:
        study_path = arg.study[0]
    else:
        raise Exception("You must call nibble with either --cfg or --study")
       
    print
    
    if arg.run:
        subjs_to_run = []
    
    # starting with spm
    total = config.yaml2data(study_path)
    ver = total['version']
    subjects = total['subjects']
    if ver == 1:
        project = total['project']
        tdl = project['todo']
        paradigms = project['paradigms']
        for stream in tdl: # only spm for now
            for paradigm in paradigms:
                for subj in subjects:
                    try:
                        if stream['name'] == 'SPM':
                            try:
                                pieces = stream['pieces']
                                spm_obj = spm.SPM(subj, paradigm, pieces, total)
                                if arg.run:
                                    subjs_to_run.append(spm_obj)
                                if arg.gen:
                                    spm_obj.resolve()
                                    spm_obj.dump()
                            except KeyError:
                                raise config.SpecError("""Each stream must have a pieces key""")
                    except KeyError:
                        raise config.SpecError("""Each stream in the project's todo
                                        field needs a name key""")
    if arg.run:
        if use_joblib:
            Parallel(n_jobs=arg.ncpu)(delayed(run_subject)(subj) for subj in subjs_to_run)
        else:
            [subj.run() for subj in subjs_to_run] 
