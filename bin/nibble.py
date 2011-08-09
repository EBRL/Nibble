#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

from argparse import ArgumentParser


from nibble import config
reload(config)
from nibble import spm
reload(spm)

from pdb import set_trace

DEBUG = False

test_config = ['/Users/scottburns/Code/Nibble/config/cutting.yaml',
                '/Users/scottburns/Code/Nibble/config/LDRC_KKI/LDRC_KKI.yaml',
                '/Users/scottburns/Code/Nibble/config/LDRC_KKI/subjects.yaml']

def parse_args():

    ap = ArgumentParser(description='nibble [options]')
    
    #add arguments
    ap.add_argument('--cfg', nargs='+', default=[])
    ap.add_argument('--study', nargs=1, default='')
    return ap.parse_args()
    

    
if __name__ == '__main__':

    arg = parse_args()

    #starting with config
    if len(arg.cfg) > 0:
        cfg = config.Configurator(args.cfg, verbose=1)
        study_path = cfg.save()
    elif arg.study:
        study_path = arg.study
    else:
        raise Error("You must call nibble with either --cfg or --study")
       
    print
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
                                spm_obj.resolve()
                                spm_obj.dump()
                                print
                            except KeyError:
                                raise config.SpecError("""Each stream must have a pieces key""")
                    except KeyError:
                        raise config.SpecError("""Each stream in the project's todo
                                        field needs a name key""")
                                        
