# -*- coding: utf-8 -*-
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bcp47',
    version='0.0.2',
    author='Jonas Byström',
    author_email='highfestiva@gmail.com',
    description='Language tags made easy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/highfestiva/bcp47.py',
    packages=['bcp47'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
