import configparser
from pathlib import Path
from typing import List

import pytest
from packaging.requirements import Requirement

SETUP_CFG_FILE = Path(__file__).parent.parent / "setup.cfg"


@pytest.fixture(scope="session")
def cfg_requirements() -> List[Requirement]:
    """A fixture for getting the requirements of from setup.cfg."""
    parser = configparser.ConfigParser()
    parser.read(SETUP_CFG_FILE)

    return [
        Requirement(line)
        for line in parser.get("options", "install_requires").splitlines()
        if line
    ]
