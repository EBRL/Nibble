#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""
import os
from os.path import join as pj
from warnings import warn
import pdb
from pprint import pprint

from pdb import set_trace


try:
    import yaml
except ImportError:
    print "You must install PyYAML."
    raise

class SpecError(Exception):
    pass

def yaml2data(filename, verbose=0):
    """Main function for load yaml files
    """
    data = {}
    with open(filename, 'r') as f:
        if verbose > 4:
            print('Parsing yaml from %s' % filename)
        try:
            data = yaml.load(f)
        except yaml.YAMLError, exc:
            print('Parsing error in %s:' % filename)
            print_yamlerror(exc)
            raise
        else:
            return data

def data2yaml(data, filename, verbose=0):
    """Main function for dumping data to a yaml filename

    Parameters
    ----------
    data: object
        python object to save in yaml file
    filename: str
        path to file in which data will be saved in yaml
    """
    try:
        with open(filename, 'w') as f:
            yaml.dump(data, f)
            if verbose > 0:
                print("Saved data to %s" % filename)
    except IOError:
        print('Error when dumping data to %s' % filename)
        raise

def print_yamlerror( exc):
    """Try to help user spot bug by printing line/column information of
    parsing error"""
    if hasattr(exc, 'problem_mark'):
        mark = exc.problem_mark
        print('Error position: (%s:%s)' % (mark.line+1, mark.column+1))

class Configurator(object):
    """ Main class for combining multiple yaml files to one data structure
    """
    def __init__(self, yaml_file_list, verbose=10):
        """ Constructor

        Parameters
        ----------
        yaml_file_list: seq
            all yaml files that should be coerced into one data structure
        output_path: str
            path to final data structure
        verbose: int
            verbosity level
        """
        exist = map(os.path.isfile, yaml_file_list)
        if not all(exist):
            raise IOError('Not all files specified in the constructor exist')
        self.yaml_files = yaml_file_list

        # add the nibble.yaml2data
        user_nibble = os.path.expanduser('~/.nibble.yaml')
        if os.path.isfile(user_nibble):
            self.yaml_files.append(user_nibble)
        self.verbose = verbose
        self.load_yaml()

    def load_yaml(self):
        """ Load all yaml files
        """
        all_data = {}
        for yaml_file in self.yaml_files:
            try:
                doc_data = yaml2data(yaml_file, self.verbose)
            except yaml.YAMLError:
                raise
            else:
                if 'version' in doc_data:
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
                else:
                    warn("No version in %s" % yaml_file)
        if self.verbose > 10:
            print('Here is the complete data structure...')
            pprint(all_data)
        self.all_data = all_data

    def save(self):
        """Save the complete data spec as yaml"""
        if ('config' in self.all_data['nibble'] and
            'output_path' in self.all_data['nibble']['config']):
            output_fname = '%s.yml' % self.all_data['project']['name']
            output_path = os.path.expanduser(pj(self.all_data['nibble']['config']['output_path'],
                            output_fname))
            data2yaml(self.all_data, output_path, self.verbose)
        else:
            raise SpecError('config_output_path not set in nibble.yaml')
        return output_path
