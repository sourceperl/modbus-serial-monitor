# -*- coding: utf-8 -*-

from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='modbus_serial_monitor',
    version='0.0.1',
    description='A set of tools for modbus diagnostic',
    long_description='',
    author='Loic Lefebvre',
    author_email='loic.celine@free.fr',
    license='MIT',
    url='https://github.com/sourceperl/modbus-serial-monitor',
    platforms='any',
    install_requires=required,
    scripts=[
        'scripts/modbus-scan-serial',
        'scripts/modbus-gui',
    ],
)
