import shutil
from pathlib import Path

import pytest

REPO_PATH = Path(__file__).parent / "assets" / "test_file_based_repo"


@pytest.fixture
def random_vault(tmpdir):
    shutil.copytree(REPO_PATH, tmpdir, dirs_exist_ok=True)
    return tmpdir
