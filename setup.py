#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Scott Burns <scott.s.burns@gmail.com>'
__license__ = 'BSD 3-Clause'

import os
import nibble

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if __name__ == '__main__':

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    long_desc = "Nibble is a basic batch generation tool"

    setup(name='Nibble',
        maintainer='Scott Burns',
        maintainer_email='scott.s.burns@gmail.com',
        description="""Nibble: NeuroImaging Batch BuiLdEr""",
        license='BSD (3-clause)',
        url='http://github.com/sburns/Nibble',
        version=nibble.__version__,
        download_url='http://github.com/sburns/Nibble',
        long_description=long_desc,
        packages=['nibble'],
        requires=['yaml'],
        platforms='any',
        classifiers=(
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved',
                'Topic :: Software Development',
                'Topic :: Scientific/Engineering',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Operating System :: MacOS',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.7',)
        )
