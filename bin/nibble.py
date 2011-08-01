#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""

def test_config(input_list, output_path):
    from nibble import config
    reload(config)
    cfg = config.Configurator(input_list)
    all_data = cfg.load_yaml(verbose=False)
    cfg.save_yaml(output_path)


if __name__ == '__main__':
    input_config = ['/Users/scottburns/Documents/code/Nibble/configurations/cutting_global.yaml',
                        '/Users/scottburns/Documents/code/Nibble/configurations/LDRC_KKI.yaml']
    output_path = '/Users/scottburns/Documents/code/Nibble/configurations/LDRC_KK_final.yaml'
    test_config(input_config, output_path)
    
