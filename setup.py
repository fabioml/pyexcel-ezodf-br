#!/usr/bin/env python
# coding:utf-8
# Author:  mozman
# Purpose: setup
# Created: 27.12.2010
# License: MIT license
#
#    Copyright (C) 2010  Manfred Moitzi
#
# Previous maintainer: 'Anton Shvein'
# Contact: 't0hashvein@gmail.com'
#
import os
import sys
import codecs
from shutil import rmtree
from setuptools import setup, find_packages, Command
PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7

NAME = 'pyexcel-ezodf-br'
AUTHOR = 'Fabio Luna'
VERSION = '0.3.4.1'
EMAIL = 'fabio.luna@gmail.com'
LICENSE = 'MIT'
DESCRIPTION = (
    'A Python package to create/manipulate OpenDocumentFormat files' +
    ''
)
URL = 'https://github.com/fabioml/pyexcel-ezodf-br'
DOWNLOAD_URL = '%s/archive/0.3.4.tar.gz' % URL
FILES = ['README.rst', 'CONTRIBUTORS.rst', 'CHANGELOG.rst']
KEYWORDS = [
    'ODF',
    'OpenDocumentFormat',
    'OpenOffice LibreOffice',
    'python'
]

CLASSIFIERS = [
    'Topic :: Office/Business',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
          "License :: OSI Approved :: MIT License",
          "Development Status :: 3 - Alpha",
          "Operating System :: OS Independent",
          "Topic :: Office/Business :: Office Suites"
]

INSTALL_REQUIRES = [
    'lxml',
]

if PY26:
    INSTALL_REQUIRES.append('weakrefset')

PACKAGES = find_packages(exclude=['ez_setup', 'examples', 'tests'])
EXTRAS_REQUIRE = {
}
# You do not need to read beyond this line
PUBLISH_COMMAND = '{0} setup.py sdist bdist_wheel upload -r pypi'.format(
    sys.executable)
GS_COMMAND = ('gs pyexcel-ezodf v0.3.4 ' +
              "Find 0.3.4 in changelog for more details")
NO_GS_MESSAGE = ('Automatic github release is disabled. ' +
                 'Please install gease to enable it.')
HERE = os.path.abspath(os.path.dirname(__file__))


class PublishCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package on github and pypi'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        run_status = True
        if has_gease():
            run_status = os.system(GS_COMMAND) == 0
        else:
            self.status(NO_GS_MESSAGE)
        if run_status:
            os.system(PUBLISH_COMMAND)

        sys.exit()


def has_gease():
    """
    test if github release command is installed

    visit http://github.com/moremoban/gease for more info
    """
    try:
        import gease  # noqa
        return True
    except ImportError:
        return False


def read_files(*files):
    """Read files into setup"""
    text = ""
    for single_file in files:
        content = read(single_file)
        text = text + content + "\n"
    return text


def read(afile):
    """Read a file into setup"""
    with codecs.open(afile, 'r', 'utf-8') as opened_file:
        content = filter_out_test_code(opened_file)
        content = "".join(list(content))
        return content


def filter_out_test_code(file_handle):
    found_test_code = False
    for line in file_handle.readlines():
        if line.startswith('.. testcode:'):
            found_test_code = True
            continue
        if found_test_code is True:
            if line.startswith('  '):
                continue
            else:
                empty_line = line.strip()
                if len(empty_line) == 0:
                    continue
                else:
                    found_test_code = False
                    yield line
        else:
            for keyword in ['|version|', '|today|']:
                if keyword in line:
                    break
            else:
                yield line


if __name__ == '__main__':
    setup(
        name=NAME,
        author=AUTHOR,
        version=VERSION,
        author_email=EMAIL,
        description=DESCRIPTION,
        url=URL,
        download_url=DOWNLOAD_URL,
        long_description=read_files(*FILES),
        license=LICENSE,
        keywords=KEYWORDS,
        extras_require=EXTRAS_REQUIRE,
        tests_require=['nose'],
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        classifiers=CLASSIFIERS,
        cmdclass={
            'publish': PublishCommand,
        }
    )
