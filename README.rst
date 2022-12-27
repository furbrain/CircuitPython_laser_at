Introduction
============


.. image:: https://github.com/furbrain/CircuitPython_laser_at/workflows/Build%20CI/badge.svg
    :target: https://github.com/furbrain/CircuitPython_laser_at/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Driver for an inexpensive laser rangefinder module, made by Hi-AT, available on `aliexpress
<https://www.aliexpress.com/item/32792768667.html>`_


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-laser-at/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-laser-at

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-laser-at

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-laser-at

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install laser_at

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. todo:: Add a quick, simple example. It and other examples should live in the
examples folder and be included in docs/examples.rst.

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-laser-at.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/furbrain/CircuitPython_laser_at/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
