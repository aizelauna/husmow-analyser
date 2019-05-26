# Husmow tools

Tools to gather and analyse statistics from Husqvarna automowers

## husmow-cron

### Getting Started

```sh
$ git clone https://github.com/aizelauna/husmow-analyser.git
$ cd husmow-analyser
$ poetry install
```

### Cron install

```shell
# Install logger cron script
$ crontab -e
0 0 * * * /<path>/<to>/husmow-cron  <logs output dir>
```

*husmow-cron* launches *husmow_logger* for 24 hours and configures it to
store logs to files whose name has the pattern `husmow-<date>.csv`.

All these files are the inputs of the logs analyser.


### Running Tests

```sh
$ git clone https://github.com/aizelauna/husmow-analyser.git
$ cd husmow-analyser

$ pyenv install 3.6.9
$ pyenv local 3.6.9

$ poetry install
$ poetry run pytest -v
```

Code coverage can be checked with this command:

```
$ poetry run pytest --cov husmowcron --cov-report html
```

### Prerequisites

```sh
# Ubuntu
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# Install pyenv
$ curl https://pyenv.run | bash

# Install poetry
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

## logs analyser
