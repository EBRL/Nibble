#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

from nibble import config
reload(config)
from nibble import spm
reload(spm)


if __name__ == '__main__':
    input_config = ['/Users/scottburns/Documents/code/Nibble/configurations/cutting_global.yaml',
                        '/Users/scottburns/Documents/code/Nibble/configurations/LDRC_KKI.yaml']
    output_path = '/Users/scottburns/Documents/code/Nibble/configurations/generated/LDRC_KKI_final.yaml'

    #starting with config
    cfg = config.Configurator(input_config)
    all_data = cfg.load_yaml(verbose=False)
    cfg.save_yaml(output_path)
        
    print('')
    print('')
    
    # starting with SPM
    total = config.yaml2data(output_path)
    ver = total['version']
    if ver == 1:
        project = total['project']
        tdl = project['todo']
        paradigms = project['paradigms']
        subjects = project['subjects']
        for stream in tdl: # only spm for now
            pieces = tdl[stream]
            for piece in pieces:
                for paradigm in paradigms:
                    for subj in subjects:
                        if stream == 'SPM':
                            spm_obj = spm.SPM(subj, paradigm, piece, total)
                            spm_obj.resolve()
                            spm_obj.dump()
