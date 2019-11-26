This is a meta-package which can be used in ``pyproject.toml`` files to
automatically provide the oldest supported version of Numpy without having to
list them all. In other words::

    [build-system]
    requires = [
        "wheel",
        "setuptools",
        "numpy==1.13.3; python_version=='3.5',
        "numpy==1.13.3; python_version=='3.6',
        "numpy==1.14.5; python_version=='3.7',
        "numpy==1.17.3; python_version>='3.8'
    ]

can be replaced by::

    [build-system]
    requires = ["wheel", "setuptools", "oldest-supported-numpy"]

And as new Python versions are released, the ``pyproject.toml`` file does not
need to be updated.
