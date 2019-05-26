#!/usr/bin/python3

import argparse
import configparser
import datetime
import logging
import os
import subprocess

if 'HOME' not in os.environ:
    print('$HOME variable should be set in script environment')
    exit(1)

CONFIG_PATH = os.path.join(
    os.environ['HOME'], '.config', 'husmow-cron')
if not os.path.isdir(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, 'config.ini')

DATA_PATH = os.path.join(
    os.environ['HOME'], '.local', 'share', 'husmow-cron')
if not os.path.isdir(DATA_PATH):
    os.makedirs(DATA_PATH)


def load_credentials():
    # load credentials from environment
    login = os.environ.get('AMC_LOGIN')
    password = os.environ.get('AMC_PASSWORD')
    if login and password:
        return login, password

    # load credentials from config file
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    try:
        login = config['credentials']['login']
        password = config['credentials']['password']
    finally:
        if login and password:
            return login, password

    # no credentials found
    logging.error("No credentials found")
    exit(1)


def create_authentication_token(login, password, token_dir):
    subprocess.run(
        "husmow --login {} --password {}".format(login, password),
        shell=True, cwd=token_dir)


def log_husmow_data(token_dir, logs_dir):
    iso_date = datetime.date.today().isoformat()
    csv_filename = "husmow-{}.csv".format(iso_date)
    csv_path = os.path.join(logs_dir, csv_filename)
    subprocess.run(
        "husmow_logger -f {}".format(csv_path),
        shell=True, cwd=token_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "logs_dir",
        help="directory where to store mower logs")
    args = parser.parse_args()

    login, password = load_credentials()

    create_authentication_token(login, password, DATA_PATH)

    log_husmow_data(DATA_PATH, args.logs_dir)


if __name__ == '__main__':
    main()
