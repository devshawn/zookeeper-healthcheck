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

from __future__ import unicode_literals

import logging
import signal
import sys
from functools import partial

from zookeeper_healthcheck import handler
from zookeeper_healthcheck import health
from zookeeper_healthcheck import parser

try:
    from SocketServer import TCPServer as HTTPServer
except ImportError:
    from http.server import HTTPServer


def main():
    config_parser = parser.get_parser()
    args = config_parser.parse_args()

    logging.basicConfig(format="%(asctime)s.%(msecs)03d [%(levelname)7s] - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=args.log_level)

    health_object = health.Health(args.zookeeper_host, args.zookeeper_port, args.healthy_modes.split(","))
    request_handler = partial(handler.RequestHandler, health_object)

    HTTPServer.allow_reuse_address = True
    httpd = HTTPServer(("", args.healthcheck_port), request_handler)
    logging.info("Serving requests at http://localhost:{}".format(args.healthcheck_port))

    def stop(status_code, frame):
        logging.info("SIGINT/SIGTERM; exiting...")
        httpd.server_close()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        stop(0, None)


if __name__ == "__main__":
    main()
