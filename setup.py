#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'haralyzer', 'pandas']

setup_requirements = []

test_requirements = []

setup(
    author="Paul Wilson",
    author_email='paulalexwilson@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Parses a VMAP document and HAR trace and generates a client behaviour report",
    entry_points={
        'console_scripts': [
            'vmap_knife=vmap_knife.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='vmap_knife',
    name='vmap_knife',
    packages=find_packages(include=['vmap_knife', 'vmap_knife.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/paulalexwilson/vmap_knife',
    version='0.1.0',
    zip_safe=False,
)
