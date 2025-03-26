import xml.etree.ElementTree as ET
from pathlib import Path

import tomli

import ndarray_msg_utils

PROJECT_ROOT = Path(__file__).parent.parent


def test_version():
    assert isinstance(ndarray_msg_utils.__version__, str)
    with open(PROJECT_ROOT / "pyproject.toml", "rb") as f:
        pyproject = tomli.load(f)
    assert pyproject["project"]["version"] == ndarray_msg_utils.__version__

    ros_pkg_version = (
        ET.parse(PROJECT_ROOT / "package.xml").getroot().find("version").text
    )
    assert ros_pkg_version is not None
    assert ros_pkg_version == ndarray_msg_utils.__version__
