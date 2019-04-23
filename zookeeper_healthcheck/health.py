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
import subprocess


class Health:

    def __init__(self, zookeeper_host, zookeeper_port, healthy_modes):
        self.zookeeper_host = zookeeper_host
        self.zookeeper_port = zookeeper_port
        self.healthy_modes = [x.lower().strip() for x in healthy_modes]
        self.log_initialization_values()

    def get_health_result(self):
        try:
            is_ok = self.is_zookeeper_ok()
            is_in_healthy_mode = self.is_zookeeper_in_healthy_mode()
            is_healthy = is_ok and is_in_healthy_mode
            health_result = {"healthy": is_healthy, "is_ok": is_ok, "is_in_healthy_mode": is_in_healthy_mode}
        except Exception as ex:
            logging.error("Error while attempting to calculate health result. Assuming unhealthy. Error: {}".format(ex))
            logging.error(ex)
            health_result = {
                "healthy": False,
                "message": "Exception raised while attempting to calculate health result, assuming unhealthy.",
                "error": "{}".format(ex)
            }
        return health_result

    def log_initialization_values(self):
        logging.info("Server will report healthy for modes: '{}'".format(", ".join(self.healthy_modes)))
        logging.info("Server will healthcheck against zookeeper host: {}".format(self.zookeeper_host))
        logging.info("Server will healthcheck against zookeeper port: {}".format(self.zookeeper_port))

    def is_zookeeper_ok(self):
        process_one = subprocess.Popen(["echo", "ruok"], stdout=subprocess.PIPE)
        process_two = subprocess.Popen(["nc", "{}".format(self.zookeeper_host), "{}".format(self.zookeeper_port)],
                                       stdin=process_one.stdout,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        process_one.stdout.close()
        (output, err) = process_two.communicate()
        exit_code = process_two.wait()
        output = output.decode("utf-8").strip()
        if exit_code == 0:
            is_ok = output == "imok"
            if is_ok:
                logging.info("ZooKeeper isok check returned response: {}".format(output))
            else:
                logging.warning("ZooKeeper isok is not healthy: {}".format(output))
            return is_ok
        else:
            logging.warning("ZooKeeper isok returned exit code: {}, marking unhealthy...".format(exit_code))
            return False

    def is_zookeeper_in_healthy_mode(self):
        process_one = subprocess.Popen(["echo", "stat"], stdout=subprocess.PIPE)
        process_two = subprocess.Popen(["nc", "{}".format(self.zookeeper_host), "{}".format(self.zookeeper_port)],
                                       stdin=process_one.stdout,
                                       stdout=subprocess.PIPE)
        process_three = subprocess.Popen(["grep", "Mode"],
                                         stdin=process_two.stdout,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        process_one.stdout.close()
        process_two.stdout.close()
        (output, err) = process_three.communicate()
        exit_code = process_three.wait()
        output = output.decode("utf-8").strip()

        if exit_code == 0:
            is_in_healthy_mode = any(mode in output for mode in self.healthy_modes)
            if is_in_healthy_mode:
                logging.info("ZooKeeper mode returned response: {}".format(output))
            else:
                logging.warning("ZooKeeper is not in a healthy mode: {}".format(output))
            return is_in_healthy_mode
        else:
            logging.warning("ZooKeeper mode returned exit code: {}, marking unhealthy...".format(exit_code))
            return False
