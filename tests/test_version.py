import tomllib
from pathlib import Path

import ndarray_msg_utils

PROJECT_ROOT = Path(__file__).parent.parent


def test_version():
    assert isinstance(ndarray_msg_utils.__version__, str)
    with open(PROJECT_ROOT / "pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    assert pyproject["project"]["version"] == ndarray_msg_utils.__version__
