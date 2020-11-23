.. image:: https://img.shields.io/pypi/v/oldest-supported-numpy
   :target: https://pypi.org/project/oldest-supported-numpy/
   :alt: PyPI

About
-----

This is a meta-package which can be used in ``pyproject.toml`` files
to automatically provide as a build-time dependency the oldest version
of Numpy that supports the given Python version and platform. In case
of platforms for which Numpy has prebuilt wheels, the provided version
also has a prebuilt Numpy wheel.

The reason to use the oldest available Numpy version as a build-time
dependency is because of ABI compatibility. Binaries compiled with old
Numpy versions are binary compatible with newer Numpy versions, but
not vice versa. This meta-package exists to make dealing with this
more convenient, without having to duplicate the same list manually in
all packages requiring it.

In other words:

.. code:: toml

    [build-system]
    requires = [
        "wheel",
        "setuptools",
        "numpy==1.13.3; python_version=='3.5'",
        "numpy==1.13.3; python_version=='3.6'",
        "numpy==1.14.5; python_version=='3.7'",
        # more numpy requirements...
    ]

can be replaced by:

.. code:: toml

    [build-system]
    requires = ["wheel", "setuptools", "oldest-supported-numpy"]

And as new Python versions are released, the ``pyproject.toml`` file does not
need to be updated.

Q&A
---

Why define the Numpy pinnings using install_requires in this repository?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Numpy version pinnings are defined inside the ``setup.cfg`` file as
``install_requires`` dependencies, rather than as build-time dependencies
inside ``pyproject.toml``. This is deliberate, since Numpy is not actually
required to build wheels of **oldest-supported-numpy**. What we need here
is to make sure that when **oldest-supported-numpy** is installed into
the build environment of a package using it, Numpy gets installed too
as a **runtime** dependency inside the build environment.

Another way to think about this is that since we only publish (universal)
wheels of **oldest-supported-numpy**, the wheel contains no ``pyproject.toml``,
``setup.cfg``, or ``setup.py`` code - it only contains metadata including
dependencies which get installed by pip when **oldest-supported-numpy** is
installed.

Can I use this if my package requires a recent version of Numpy?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In many cases, even though your package may require a version of
Numpy that is more recent than the pinned versions here, this
is often a runtime requirement, i.e. for running (rather than
building) your package. In many cases, unless you use recent
features of the Numpy C API, you will still be able to build your
package with an older version of Numpy and therefore you will still
be able to use **oldest-supported-numpy**. You can still impose a
more recent Numpy requirement in ``install_requires``

What about having a catchier name for this package?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The current name is not very catchy as package names go, but it
is very descriptive. This package is only meant to be used in
``pyproject.toml`` files for defining build-time dependencies,
so it's more important to have a descriptive than a catchy name!

What if I think that one of the pinnings is wrong or out of date?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please feel free to `open an issue <https://github.com/scipy/oldest-supported-numpy/issues/new>`_
or a pull request if you think something is wrong or could be improved!
