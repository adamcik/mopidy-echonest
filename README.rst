****************************
Mopidy-Echonest
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Echonest.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Echonest/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-Echonest.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Echonest/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/adamcik/mopidy-echonest/master.png?style=flat
    :target: https://travis-ci.org/adamcik/mopidy-echonest
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/adamcik/mopidy-echonest/master.svg?style=flat
   :target: https://coveralls.io/r/adamcik/mopidy-echonest?branch=master
   :alt: Test coverage

Echonest integration for Mopidy. Current version only supports using Echonest
as the local library backend.

State of this extension is early ALPHA, do not expect things to work just yet.

Installation
============

Install by running::

    pip install Mopidy-Echonest

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Echonest to your Mopidy configuration file::

    [echonest]
    apikey = YOUR_API_KEY


Project resources
=================

- `Source code <https://github.com/adamcik/mopidy-echonest>`_
- `Issue tracker <https://github.com/adamcik/mopidy-echonest/issues>`_
- `Download development snapshot <https://github.com/adamcik/mopidy-echonest/archive/master.tar.gz#egg=Mopidy-Echonest-dev>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
