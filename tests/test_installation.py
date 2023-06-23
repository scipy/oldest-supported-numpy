"""Test that version that gets installed (where we can run CI)
matches the expectation defined in setup.cfg"""


def test_valid_numpy_is_installed(cfg_requirements):
    filtered_requirements = []
    for req in cfg_requirements:
        if req.marker.evaluate():
            filtered_requirements.append(req)

    assert (len(filtered_requirements) == 1), "Expected exactly one pin."

    item, = filtered_requirements[0].specifier

    import numpy
    assert item.version == numpy.__version__
