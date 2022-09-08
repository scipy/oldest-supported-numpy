.. image:: https://img.shields.io/pypi/v/oldest-supported-numpy
   :target: https://pypi.org/project/oldest-supported-numpy/
   :alt: PyPI

About
-----

This is a meta-package which can be used in ``pyproject.toml`` files
to automatically provide as a build-time dependency the oldest version
of NumPy that supports the given Python version and platform. In case
of platforms for which NumPy has prebuilt wheels, the provided version
also has a prebuilt NumPy wheel.

The reason to use the oldest available NumPy version as a build-time
dependency is because of ABI compatibility. Binaries compiled with old
NumPy versions are binary compatible with newer NumPy versions, but
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

Why define the NumPy pinnings using ``install_requires`` in this repository?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The NumPy version pinnings are defined inside the ``setup.cfg`` file as
``install_requires`` dependencies, rather than as build-time dependencies
inside ``pyproject.toml``. This is deliberate, since NumPy is not actually
required to build wheels of **oldest-supported-numpy**. What we need here
is to make sure that when **oldest-supported-numpy** is installed into
the build environment of a package using it, NumPy gets installed too
as a **runtime** dependency inside the build environment.

Another way to think about this is that since we only publish (universal)
wheels of **oldest-supported-numpy**, the wheel contains no ``pyproject.toml``,
``setup.cfg``, or ``setup.py`` code - it only contains metadata including
dependencies which get installed by pip when **oldest-supported-numpy** is
installed.

Can I use this if my package requires a recent version of NumPy?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In many cases, even though your package may require a version of
NumPy that is more recent than the pinned versions here, this
is often a runtime requirement, i.e. for running (rather than
building) your package. In many cases, unless you use recent
features of the NumPy C API, you will still be able to build your
package with an older version of NumPy and therefore you will still
be able to use **oldest-supported-numpy**. You can still impose a
more recent NumPy requirement in ``install_requires``

What if a bug in NumPy that affects me is fixed only in a newer release?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If **oldest-supported-numpy** pins a ``numpy`` version that is broken for
everyone using a certain OS/platform/interpreter combination, we can update the
``==`` pin to a newer release. In general, building against a newer *bugfix*
release (i.e., a higher ``Y`` value for a ``1.X.Y`` version number) is safe to
do. Newer minor versions will likely not be ABI-compatible, so are much more
difficult to change. If a bug only affects some uses cases (e.g., versions ``<
1.20.3`` don't work on Windows when using ``f2py``), the pin cannot be updated
because it will affect backwards compatibility of **oldest-supported-numpy**.
In that case, it is recommended that you add the needed constraint directly
in your own ``pyproject.toml`` file. For example:

.. code:: toml

    [build-system]
    requires = [
        "wheel",
        "numpy==1.19.0; python_version<='3.8' and platform_system=='Windows' and platform_python_implementation != 'PyPy'",
        "oldest-supported-numpy; python_version>'3.8' or platform_system!='Windows' or platform_python_implementation == 'PyPy'",
        # more requirements (if needed) ...
    ]

Note that when you do this, it is important to ensure the conditions are such
that there is exactly one pin possible for a given platform configuration.
Otherwise your build will fail or ``pip`` may refuse to install your package
*only* on that configuration (so you likely won't see it in CI).
The **oldest-supported-numpy** repository contains tests, so for safety you
may want to implement your constraints in its ``setup.cfg`` and run the
tests with ``pytest`` to validate those constraints.

Why isn't ``oldest-supported-numpy`` available for Conda, Homebrew, Debian, etc.?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``pyproject.toml`` format is specific to PyPI. Other packaging systems have
their own metadata formats and ways of specifying dependencies. Typically they
don't need anything like **oldest-supported-numpy** because either (a) they ship
only a single NumPy version for a given release (typically the case for Linux
distros and Homebrew), or (b) they have a more explicit way of managing ABI
compatibility (see for example conda-forge's ``pin_compatible`` feature:
https://conda-forge.org/docs/maintainer/knowledge_base.html#linking-numpy).

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
