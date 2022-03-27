"""Tests to ensure that the dependency declarations are sane.
"""

import configparser
import pprint
from functools import cache
from pathlib import Path

import pytest
from packaging.requirements import Requirement

SETUP_CFG_FILE = Path(__file__).parent.parent / "setup.cfg"


def is_pinned(requirement: Requirement) -> bool:
    return "==" in str(requirement.specifier)


@cache
def get_package_dependencies() -> list[Requirement]:
    """A cached reader for getting dependencies of this package."""
    parser = configparser.ConfigParser()
    parser.read(SETUP_CFG_FILE)

    return [
        Requirement(line)
        for line in parser.get("options", "install_requires").splitlines()
        if line
    ]


# The ordering of these markers is important, and is used in test names.
# The tests, when run, look like: PyPy-3.6-Linux-aarch64` (bottom-first)
@pytest.mark.parametrize("platform_machine", ["x86_64", "aarch64", "s390x", "arm64", "loongarch64"])
@pytest.mark.parametrize("platform_system", ["Linux", "Windows", "Darwin", "AIX"])
@pytest.mark.parametrize("python_version", ["3.6", "3.7", "3.8", "3.9", "3.10", "3.11"])
@pytest.mark.parametrize("platform_python_implementation", ["CPython", "PyPy"])
def test_has_at_most_one_pinned_dependency(
    platform_machine,
    platform_system,
    python_version,
    platform_python_implementation,
):
    # These are known to be platforms that are not valid / possible at this time.
    if platform_system == "AIX":
        if platform_machine in ["aarch64", "loongarch64"]:
            pytest.skip("AIX and aarch64 are mutually exclusive.")
        if platform_python_implementation == "PyPy":
            pytest.skip("AIX and PyPy are mutually exclusive.")

    if platform_python_implementation == "PyPy" and (platform_machine not in ["x86_64", "aarch64"]):
        pytest.skip(f"PyPy is not supported on {platform_machine}.")

    environment = {
        "python_version": python_version,
        "platform_python_implementation": platform_python_implementation,
        "platform_machine": platform_machine,
        "platform_system": platform_system,
    }

    filtered_requirements = []
    for req in get_package_dependencies():
        assert req.marker
        if not req.marker.evaluate(environment):
            continue
        if not is_pinned(req):
            continue

        filtered_requirements.append(req)

    assert (
        len(filtered_requirements) <= 1
    ), f"Expected no more than one pin.\n{pprint.pformat(environment)}"
