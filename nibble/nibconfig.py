#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""
import os 
from warnings import warn
import pdb

try:
    import yaml
except ImportError:
    print "You must install PyYAML."
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
        self.yaml_files = yaml_file_list
    
    def load_yaml(self):
        """ Load all yaml files
        """
        all_data = {}
        for yaml_file in self.yaml_files:
            with open(yaml_file, 'r') as f:
                doc_data = yaml.load(f)
                try:
                    #pdb.set_trace()
                    doc_ver = doc_data['version']
                    if 'version' in all_data:
                        if doc_ver != all_data['version']:
                            all_doc['version'] = doc_ver
                            warn("Different config versions!")
                    else: #update version
                        all_data['version'] = doc_ver
                    if doc_ver == 1:
                        # in ver 1, no documents, so just copy top most keys into
                        # dict
                        doc_keys = filter(lambda x: x != "version", doc_data.keys())
                        for key in doc_keys:
                            if key in all_data:
                                warn("Top-level key collision!")
                            all_data[key] = doc_data[key]
                except KeyError: # no 'version' in document
                    warn("No version in %s" % yaml_file)
        print('Done')
        return all_data
