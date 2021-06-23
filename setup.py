#!/usr/bin/python3

from setuptools import setup

config = {
    "description": "Meeting agenda builder",
    "author": "Stuart Prescott",
    "url": "http://www.complexfluids.net/",
    "download_url": "http://www.complexfluids.net/",
    "author_email": "s.prescott@unsw.edu.au",
    "version": "0.1",
    "install_requires": [
        "python-docx",
        "ruamel.yaml",
        "PyPDF2",
        "reportlab",
    ],
    "packages": ["agendabuilder"],
    "name": "agendabuilder",
    "scripts": ["bin/agenda-builder.py"],
}

setup(**config)
