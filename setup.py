import os
from setuptools import setup, find_packages

from app import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = []

setup(
    name = "Roshamboo Service",
    version = ".".join(map(str, __version__)),
    description = "",
    long_description = read('README.md'),
    url = '',
    license = 'MIT',
    author = 'Anakin Thanainantha',
    author_email = 'anakin.t@mail.kmutt.ac.th',
    packages = find_packages(exclude=['tests']),
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    install_requires = requirements,
    tests_require = [],
)
