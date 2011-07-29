#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

    


if __name__ == '__main__':
    import nibconfig
    reload(nibconfig)
    cfg = nibconfig.Configurator(['/Users/scottburns/Documents/code/nibble/configurations/cutting_global.yaml',
                        '/Users/scottburns/Documents/code/nibble/configurations/LDRC_KKI.yaml'])
    all_data = cfg.load_yaml()
