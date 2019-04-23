import pytest

from .context import zookeeper_healthcheck

test_data = [
    "0.0.1",
    "2.1.3",
]


@pytest.mark.parametrize("test_input", test_data)
def test_get_version(test_input):
    old_version = zookeeper_healthcheck.version.__version__
    zookeeper_healthcheck.version.__version__ = test_input
    assert zookeeper_healthcheck.version.get_version() == test_input
    zookeeper_healthcheck.version.__version__ = old_version
