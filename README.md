# husmow-analyser

## logs capture

```shell
# Install pyhusmow
$ virtualenv -p python3 husmow_venv
$ source husmow_venv/bin/activate
$ pip3 install pyhusmow

# Install husmow-cron script
$ sudo cp husmow-cron /usr/bin
$ sudo chmod +x /usr/bin/husmow-cron

# Install cron script
$ crontab -e
0 0 * * * husmow-cron "husmow-venv directory" "logs output directory"
```

*husmow-cron* launches *husmow_logger* for 24 hours and configures it to store logs to files whose name has the pattern `husmow-<date>.csv`.

It will also add this filename to the file *husmow.list*.

All these files are the inputs of the logs analyser.

## logs analyse
