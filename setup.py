#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-loopreturns",
    version="0.1.0",
    description="Singer.io tap for extracting Loop Returns data",
    author="Loop Returns",
    url="http://loopreturns.com",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_loopreturns"],
    install_requires=[
        "singer-python==5.9.0",
        "requests==2.24.0",
    ],
    extras_require={
        'dev': [
            'pylint==2.6.0',
            'ipdb==0.13.3',
            'nose==1.3.7'
        ]
    },
    entry_points="""
    [console_scripts]
    tap-loopreturns=tap_loopreturns:main
    """,
    packages=["tap_loopreturns"],
    package_data={
        "schemas": ["tap_loopreturns/schemas/*.json"]
    },
    include_package_data=True,
)
