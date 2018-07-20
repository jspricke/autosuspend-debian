Installation instructions
=========================

|project_program| is designed for Python **3** and does not work with Python 2.

Requirements
------------

The minimal requirements are.

* `Python 3`_
* `psutil`_

Additionally, the some checks need further dependencies to function properly.
Please refer to :ref:`available-checks` for individual requirements.

If checks using URLs to load data should support ``file://`` URLs, `requests-file`_ is needed.

Binary packages
---------------

Debian (testing)
~~~~~~~~~~~~~~~~~

Installation from official package sources::

    apt-get install autosuspend

Archlinux (AUR)
~~~~~~~~~~~~~~~

|project| is available as an `Archlinux AUR package <https://aur.archlinux.org/packages/autosuspend/>`_.

Installation via :program:`pacaur`::

    pacaur -S autosuspend

Other distributions
~~~~~~~~~~~~~~~~~~~

In case you want to generate a package for a different Linux distribution, I'd be glad to hear about that.

From-source installation
------------------------

|project_program| provides a usual :file:`setup.py` file for installation using common `setuptools`_ methods.
Briefly, the following steps are necessary to install |project_program|:

.. code-block:: bash

   git clone https://github.com/languitar/autosuspend.git
   cd autosuspend
   python3 setup.py install # with desired options

To build the documentation, the following command can be used:

.. code-block:: bash

   python3 setup.py build_sphinx
