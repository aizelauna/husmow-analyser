import argparse
import configparser
import datetime
import os.path
import subprocess
import tempfile
import sys


def test_env_credentials(monkeypatch):
    # add environment variables
    monkeypatch.setenv('AMC_LOGIN', 'husmow-env-login')
    monkeypatch.setenv('AMC_PASSWORD', 'husmow-env-password')

    # load and test credentials
    import husmowcron.main
    login, password = husmowcron.main.load_credentials()

    assert login == 'husmow-env-login'
    assert password == 'husmow-env-password'


def test_config_credentials(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # write config file
        config_path = os.path.join(tmpdirname, '.config', 'husmow-cron')
        config_file_path = os.path.join(config_path, "config.ini")
        config = configparser.ConfigParser()
        config['credentials'] = {
            'login': 'husmow-config-login',
            'password': 'husmow-config-password'}
        os.makedirs(config_path)
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)

        # patch HOME variable and unload husmowcron modules
        monkeypatch.setenv('HOME', tmpdirname)
        sys.modules.pop('husmowcron.main', None)
        import husmowcron.main

        # load and test credentials
        login, password = husmowcron.main.load_credentials()

        # unpatch HOME variable and unload husmowcron modules
        monkeypatch.setenv('HOME', '')
        sys.modules.pop('husmowcron.main', None)

        assert login == 'husmow-config-login'
        assert password == 'husmow-config-password'


def run_husmow(args_list, cwd):
    husmow_parser = argparse.ArgumentParser()
    husmow_parser.add_argument('--login')
    husmow_parser.add_argument('--password')
    args = husmow_parser.parse_args(args_list)

    token_path = os.path.join(cwd, 'token.cfg')
    with open(token_path, 'w+') as f:
        print(vars(args))
        f.write('{login}-{password}'.format(**vars(args)))


def run_husmow_logger(args_list, cwd):
    husmow_logger_parser = argparse.ArgumentParser()
    husmow_logger_parser.add_argument('-f', dest='csv_path')
    args = husmow_logger_parser.parse_args(args_list)

    with open(args.csv_path, 'w+') as f:
        f.write('''
time,status,battery %,next start time,status duration,latitude,longitude
{date}T00:00:06.182347,OK_CUTTING,84,,0:00:00,43.37407833333334,1.741355
{date}T00:01:06.384081,OK_CUTTING,83,,0:01:00,43.37412666666667,1.7412233333333333
{date}T00:02:06.567081,OK_CUTTING,83,,0:02:00,43.374075,1.7412166666666666
{date}T00:03:06.822546,OK_CUTTING,82,,0:03:00,43.37404,1.7412933333333334
{date}T00:04:07.031692,OK_CUTTING,82,,0:04:01,43.374085,1.7413500000000002
'''.format(date=datetime.date.today().isoformat()))


def mock_subprocess_run(cmd_line, shell, cwd):
    tokens = cmd_line.split()
    if len(tokens) == 0:
        raise ValueError('cmd should not be empty')

    cmd = tokens[0]
    args_list = tokens[1:]

    commands = {
        'husmow': run_husmow,
        'husmow_logger': run_husmow_logger
    }
    commands[cmd](args_list, cwd)


def test_husmow_cron(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # prepare test environment
        monkeypatch.setenv('AMC_LOGIN', 'token-login')
        monkeypatch.setenv('AMC_PASSWORD', 'token-password')
        monkeypatch.setenv('HOME', tmpdirname)
        monkeypatch.setattr(sys, 'argv', ['husmow-cron', tmpdirname])
        monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
        sys.modules.pop('husmowcron.main', None)

        # run husmowcron
        import husmowcron.main
        husmowcron.main.main()

        # check that token.cfg is actually created
        token_path = os.path.join(
            tmpdirname, '.local', 'share', 'husmow-cron', 'token.cfg')
        with open(token_path) as f:
            token = f.read().strip()
        assert token == 'token-login-token-password'

        # check that some data has been logged
        for f in os.listdir(tmpdirname):
            if f.endswith('.csv'):
                csv_path = os.path.join(tmpdirname, f)
                break
        assert os.path.isfile(csv_path)

        with open(csv_path) as f:
            logs = f.readlines()
        assert len(logs) > 1
