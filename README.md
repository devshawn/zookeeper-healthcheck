# zookeeper-healthcheck

[![Build Status](https://travis-ci.org/devshawn/zookeeper-healthcheck.svg?branch=master)](https://travis-ci.org/devshawn/zookeeper-healthcheck) ![PyPI](https://img.shields.io/pypi/v/zookeeper-healthcheck.svg?color=blue) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zookeeper-healthcheck.svg) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A simple healthcheck wrapper to monitor ZooKeeper.

ZooKeeper Healthcheck is a simple server that provides a singular API endpoint to determine the health of a ZooKeeper instance. This can be used to alert or take action on unhealthy ZooKeeper instances.

The service checks the health by sending `netcat` commands as well as checking that ZooKeeper is in a desired mode. It utilizes the commands `echo ruok | nc zookeeper-host zookeeper-port` and `echo stat | nc zookeeper-host zookeeper-port | grep Mode` to do so.

By default, the root endpoint `/` will return `200 OK` healthy if ZooKeeper responds `imok` and is in mode `leader` or `follower`. It will return `503 Service Unavailable` if ZooKeeper does not respond with `imok` or if its in an undesired mode (by default `standalone`).

## Usage
ZooKeeper Healthcheck can be installed via `pip`. Both `python` and `pip` are required, as well as `echo`, `nc` and `grep`. 

### Command-Line
Install `zookeeper-healthcheck` via `pip`:

```bash
pip install zookeeper-healthcheck
```

To start the healthcheck server, run:

```bash
zookeeper-healthcheck
```

The server will now be running on [localhost:12181][localhost].

## Configuration
ZooKeeper Healthcheck can be configured via command-line arguments or by environment variables. 

#### Port
The port for the `zookeeper-healthcheck` API.

| Usage                 | Value              |
|-----------------------|--------------------|
| Environment Variable  | `HEALTHCHECK_PORT` |
| Command-Line Argument | `--port`           |
| Default Value         | `12181`            |

#### ZooKeeper Host
The host of the ZooKeeper instance to run the health check against. This is used with `nc`.

| Usage                 | Value                        |
|-----------------------|------------------------------|
| Environment Variable  | `HEALTHCHECK_ZOOKEEPER_HOST` |
| Command-Line Argument | `--zookeeper-host`           |
| Default Value         | `localhost`                  |

#### ZooKeeper Port
The port of the ZooKeeper instance to run the health check against. This is used with `nc`.

| Usage                 | Value                        |
|-----------------------|------------------------------|
| Environment Variable  | `HEALTHCHECK_ZOOKEEPER_PORT` |
| Command-Line Argument | `--zookeeper-port`           |
| Default Value         | `2181`                       |

#### Healthy Modes
A comma-separated list of ZooKeeper modes to be marked as healthy. Any modes not in this list will mark ZooKeeper as unhealthy. 

| Usage                 | Value                                       |
|-----------------------|---------------------------------------------|
| Environment Variable  | `HEALTHCHECK_HEALTHY_MODES`                 |
| Command-Line Argument | `--healthy-modes`                           |
| Default Value         | `leader,follower`                           |
| Valid Values          | `leader`, `follower`, `standalone`          |

#### Log Level
The level of logs to be shown by the application.

| Usage                 | Value                                       |
|-----------------------|---------------------------------------------|
| Environment Variable  | `HEALTHCHECK_LOG_LEVEL`                     |
| Command-Line Argument | `--log-level`                               |
| Default Value         | `INFO`                                      |
| Valid Values          | `DEBUG`, `INFO`, `WARNING`, `ERROR`         |

All healthy responses are logged at `INFO`. Unhealthy responses are logged at `WARNING`. Any unexpected errors are logged at `ERROR`.

## License
Copyright (c) 2019 Shawn Seymour.

Licensed under the [Apache 2.0 license][license].

[localhost]: http://localhost:12181
[license]: LICENSE
