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


    
if __name__ == '__main__':

    ap = ArgumentParser(description='nibble [options]')
    
    #add arguments
    ap.add_argument('-c', '--cfg', nargs='+')

    if DEBUG:
        args = "--config %s" % ' '.join(test_config)
        set_trace()
        ap.parse_args(args.split())
    args = ap.parse_args()
    #starting with config
    cfg = config.Configurator(args.cfg, verbose=1)
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
                                        
