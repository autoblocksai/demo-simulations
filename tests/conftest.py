import os
from datetime import datetime

import pytest


@pytest.fixture(scope="session", autouse=True)
def set_autoblocks_simulation_id():
    os.environ["AUTOBLOCKS_SIMULATION_ID"] = "pytest-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    yield
    del os.environ["AUTOBLOCKS_SIMULATION_ID"]
