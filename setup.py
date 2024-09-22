# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pydhgripper',
    version='0.1.0',
    description='Python library for controlling the DH gripper',
    packages=find_packages(),
    author='Yu Jie, Xudong Han',
    url='https://github.com/han-xudong/pyDHgripper',
    install_requires=[
        'crcmod==1.7',
        'pyserial==3.5',
    ],
    python_requires='>=3.6',
    keywords=['DH gripper', 'robotics', 'robotic gripper'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)