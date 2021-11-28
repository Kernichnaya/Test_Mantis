import importlib
import json
import os
import ftputil
import jsonpickle as jsonpickle
import pytest

from fixture.application import Application

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture(scope='session')
def config(request):
    return load_config(request.config.getoption('--target'))

@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption('--browser')
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(username=config['webAdmin']['username'], password=config['webAdmin']['password'])
    return fixture

@pytest.fixture(scope='session', autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--target', action='store', default='target.json')

"""
Закомментировал этот блок, потому что на версию MantisBT-2.25.2 
при регистрации нового пользователя не требуется ввод капчи

@pytest.fixture(scope='session', autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'],
                                 config['ftp']['username'],
                                 config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'],
                                     config['ftp']['username'],
                                     config['ftp']['password'])
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config/config_inc.php.bak'):
            remote.remove('config/config_inc.php.bak')
        if remote.path.isfile('config/config_inc.php'):
            remote.rename('config/config_inc.php', 'config/config_inc.php.bak')
        remote.upload(os.path.join(os.path.dirname(__file__), 'resources/config_inc.php'), "config/config_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile('config/config_inc.php.bak'):
            if remote.path.isfile('config/config_inc.php'):
                remote.remove('config/config_inc.php')
            remote.rename('config/config_inc.php.bak', 'config/config_inc.php')
"""


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith('data_'):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith('json_'):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())