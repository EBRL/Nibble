#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

def test_config():
    from nibble import config
    reload(config)
    cfg = config.Configurator(['/Users/scottburns/Documents/code/nibble/configurations/cutting_global.yaml',
                        '/Users/scottburns/Documents/code/nibble/configurations/LDRC_KKI.yaml'])
    all_data = cfg.load_yaml()



if __name__ == '__main__':
    test_config()
