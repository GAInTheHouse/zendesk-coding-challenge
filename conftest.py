import pytest
def pytest_addoption(parser):
    parser.addoption("--username", action="store", default="default name")
    parser.addoption("--password", action="store", default="default name")


@pytest.fixture(scope='session')
def name(request):
    name = request.config.option.username
    password = request.config.option.password
    if name is None:
        pytest.skip()
    return (name,password)