# -*- coding: utf-8 -*-

import os

from setuptools import find_packages
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'pinyin4py',
    version = '1.0.dev',
    description = "Convert hanzi to pinyin",
    long_description = read('doc/spec.md'),

    author = "Zhang Erning",
    url = "https://github.com/anjuke/pinyin4py",
    license='BSD',

    package_dir = {'': 'src'},
    packages = find_packages('src'),

    include_package_data = True,
    package_data = {
        '': ['*.txt']
    },

    zip_safe = False,

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
