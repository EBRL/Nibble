#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""
import os 

try:
    import yaml
except ImportError:
    print "You must install PyYAML. Try $ easy_install pyyaml"
    raise


class Configurator(object):
    """ Main class for combining multiple yaml files to one data structure
    """
    def __init__(self, yaml_file_list):
        """ Constructor
    
        Parameters
        ----------
        yaml_file_list: seq
            all yaml files that should be coerced into one data structure
        """
        exist = map(os.path.isfile, yaml_file_list)    
        if not all(exist):
            raise IOError('Not all files specified in the constructor exist')
        yaml_files = yaml_file_list
    
    
