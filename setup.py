#!/usr/bin/env python3
from sys import version_info, stderr
from setuptools import setup, find_packages

NAME = 'sharepg'
CURRENT_PYTHON = version_info[:2]
REQUIRED_PYTHON = (3, 10)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    stderr.write(
        f"{NAME} requires Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]} or higher and your current version is {CURRENT_PYTHON}.")
    exit(1)

setup(
    name=NAME,
    version='0.0.1',
    description='Variation graph simulation tool',
    url='https://github.com/Tharos-ux/sharepg',
    author='Tharos',
    author_email='dubois.siegfried@inria.fr',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license="LICENSE",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'tharos-pytools',
        'gfagraphs',
        'BubbleGun',
    ],
    entry_points={'console_scripts': ['sharepg=sharepg.main:main']}
)
