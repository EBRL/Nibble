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

    #starting with config
    cfg = config.Configurator(input_config, verbose=1)
    output_path = cfg.save()
    
    print
    print

    # starting with spm
    total = config.yaml2data(output_path)
    ver = total['version']
    subjects = total['subjects']
    if ver == 1:
        project = total['project']
        tdl = project['todo']
        paradigms = project['paradigms']
        for stream in tdl: # only spm for now
            for paradigm in paradigms:
                for subj in subjects:
                    if stream == 'SPM':
                        pieces = tdl[stream]
                        spm_obj = spm.SPM(subj, paradigm, pieces, total)
                        spm_obj.resolve()
                        spm_obj.dump()
