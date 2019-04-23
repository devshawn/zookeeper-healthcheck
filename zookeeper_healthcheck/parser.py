#  Copyright 2019 Shawn Seymour. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"). You
#  may not use this file except in compliance with the License. A copy of
#  the License is located at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
#  ANY KIND, either express or implied. See the License for the specific
#  language governing permissions and limitations under the License.

import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser(description="A simple healthcheck for ZooKeeper. It checks if ZooKeeper is 'ok' via 'ruok' and "
                                                 "checks if it is in a mode determined as healthy via 'stat'. "
                                                 "Healthy modes can be set as desired.")

    parser.add_argument("--port",
                        default=os.environ.get("HEALTHCHECK_PORT", "12181"),
                        dest="healthcheck_port",
                        type=int,
                        nargs="?",
                        help="The port for the healthcheck HTTP server."
                        )

    parser.add_argument("--zookeeper-host",
                        default=os.environ.get("HEALTHCHECK_ZOOKEEPER_HOST", "localhost"),
                        dest="zookeeper_host",
                        nargs="?",
                        help="The host of the ZooKeeper instance that the health check will be run against."
                        )

    parser.add_argument("--zookeeper-port",
                        default=os.environ.get("HEALTHCHECK_ZOOKEEPER_PORT", "2181"),
                        dest="zookeeper_port",
                        type=int,
                        nargs="?",
                        help="The port of the ZooKeeper instance that the health check will be run against."
                        )

    parser.add_argument("--healthy-modes",
                        default=os.environ.get("HEALTHCHECK_HEALTHY_MODES", "leader,follower").lower(),
                        dest="healthy_modes",
                        nargs="?",
                        help="A comma separated list of ZooKeeper modes to be marked as healthy. Default: leader,follower."
                        )

    parser.add_argument("--log-level",
                        default=os.environ.get("HEALTHCHECK_LOG_LEVEL", "INFO").upper(),
                        dest="log_level",
                        nargs="?",
                        help="The level of logs to be shown. Default: INFO.")
    return parser
