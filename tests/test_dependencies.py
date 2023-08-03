"""Tests to ensure that the dependency declarations are sane.
"""

import pprint

import pytest
from packaging.requirements import Requirement


def is_pinned(requirement: Requirement) -> bool:
    return "==" in str(requirement.specifier)


# The ordering of these markers is important, and is used in test names.
# The tests, when run, look like: PyPy-3.6-Linux-aarch64` (bottom-first)
@pytest.mark.parametrize("platform_machine", ["x86", "x86_64", "aarch64", "ppc64le", "s390x", "arm64", "loongarch64"])
@pytest.mark.parametrize("platform_system", ["Linux", "Windows", "Darwin", "AIX", "OS400"])
@pytest.mark.parametrize("python_version", ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"])
@pytest.mark.parametrize("platform_python_implementation", ["CPython", "PyPy"])
def test_has_at_most_one_pinned_dependency(
    platform_machine,
    platform_system,
    python_version,
    platform_python_implementation,
    cfg_requirements,
):
    # These are known to be platforms that are not valid / possible at this time.
    # due the the sheer variety, the default assumption is that a given combination
    # is invalid, allowing us to specify valid cases more easily below
    valid = False
    match (platform_system, platform_machine):
        case ["Linux", "arm64"]:
            valid = False  # express "everything but arm64"; called aarch64 on linux
        case ["Linux", _]:
            valid = True   # otherwise, Linux is everywhere
        case ["Darwin", ("x86_64" | "arm64")]:
            valid = True
        case ["Windows", ("x86" | "x86_64" | "arm64")]:
            valid = True
        # TODO: verify architectures for AIX/OS400
        case [("AIX" | "OS400"), ("x86" | "x86_64" | "s390x")]:
            valid = True

    # currently linux-{64, aarch64, ppc64le}, osx-64, win-64; no support for arm64 yet
    pypy_pairs = [
        ("Linux", "x86_64"),
        ("Linux", "aarch64"),
        ("Linux", "ppc64le"),
        ("Darwin", "x86_64"),
        ("Windows", "x86_64"),
    ]
    if (platform_python_implementation == "PyPy"
            and (platform_system, platform_machine) not in pypy_pairs):
        valid = False

    if platform_system == "OS400" and python_version != "3.9":
        # IBMi only supported on CPython 3.9, see gh-66
        valid = False

    environment = {
        "python_version": python_version,
        "platform_python_implementation": platform_python_implementation,
        "platform_machine": platform_machine,
        "platform_system": platform_system,
    }

    filtered_requirements = []
    for req in cfg_requirements:
        assert req.marker
        if not req.marker.evaluate(environment):
            continue
        if not is_pinned(req):
            continue

        filtered_requirements.append(req)

    # since we cannot run the installation tests on all platforms,
    # we formulate the conditions when we expect a pin
    expect_pin = False
    match (platform_system, platform_machine):
        case [("Linux" | "Darwin" | "Windows"), "x86_64"]:
            expect_pin = True  # baseline
        case [("Linux" | "Windows"), "x86"]:
            # 32 bit wheels on Linux only until numpy 1.21, but should still be compatible
            expect_pin = True
        case ["Linux", "aarch64"]:
            expect_pin = True  # as of 1.19.2
        case ["Darwin", "arm64"]:
            expect_pin = True  # as of 1.21
        # no official wheels, but register minimum compatibility
        case ["Linux", "s390x"]:
            expect_pin = True  # as of 1.17.5
        case ["Linux", "loongarch64"]:
            expect_pin = (python_version != "3.7")  # as of 1.22
        case ["AIX", ("x86" | "x86_64" | "s390x")]:
            expect_pin = True  # as of 1.16
        case ["OS400", ("x86" | "x86_64" | "s390x")]:
            # only supported on CPython 3.9, see above
            expect_pin = True  # as of 1.23.3
        # if there is no information to the contrary, we expect the default pins
        case ["Linux", "ppc64le"]:
            expect_pin = True
        case ["Windows", "arm64"]:
            expect_pin = True

    # for valid combinations, we test more strictly: expect exactly zero or one pins
    if valid:
        # we only expect a pin for released python versions
        expect_pin = False if (python_version == "3.12") else expect_pin
        log_msg = "Expected " + ("exactly one pin" if expect_pin else "no pins")
        assert (
            len(filtered_requirements) == int(expect_pin)
        ), f"{log_msg}.\n{pprint.pformat(environment)}"
    else:
        # on invalid platform / interpreter combinations, test
        # that at least we do not produce more than one pin
        assert (
            len(filtered_requirements) <= 1
        ),  f"Expected no more than one pin.\n{pprint.pformat(environment)}"
