#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

from nibble import config
reload(config)
from nibble import spm
reload(spm)

from pdb import set_trace

if __name__ == '__main__':
    input_config = ['/Users/scottburns/Code/Nibble/config/cutting.yaml',
                    '/Users/scottburns/Code/Nibble/config/LDRC_KKI/LDRC_KKI.yaml',
                    '/Users/scottburns/Code/Nibble/config/LDRC_KKI/subjects.yaml']
    output_path = '/Users/scottburns/Code/Nibble/config/generated/LDRC_KKI_final.yaml'

    #starting with config
    cfg = config.Configurator(input_config)
    all_data = cfg.load_yaml(verbose=False)
    cfg.save_yaml(output_path)
        
    print('')
    print('')
    
    # starting with SPM
    total = config.yaml2data(output_path)
    ver = total['version']
    subjects = total['subjects']
    if ver == 1:
        project = total['project']
        tdl = project['todo']
        paradigms = project['paradigms']
        subjects = project['subjects']
        for stream in tdl: # only spm for now
            for paradigm in paradigms:
                for subj in subjects:
                    if stream == 'SPM':
                        pieces = tdl[stream]
                        spm_obj = spm.SPM(subj, paradigm, pieces, total)
                        spm_obj.resolve()
                        spm_obj.dump()
