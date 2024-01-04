#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'aiohttp',
'aiofiles',
'Pillow',
'google-cloud-storage',
'boto3'
]

test_requirements = [ ]

setup(
    author="Shrinivas Deshmukh",
    author_email='shrinivas@powercred.io',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="''",
    entry_points={
        'console_scripts': [
            'document_ai=document_ai.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='document_ai',
    name='document_ai',
    packages=find_packages(include=['document_ai', 'document_ai.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/PowerCred/document_ai',
    version='0.1.1',
    zip_safe=False,
)
