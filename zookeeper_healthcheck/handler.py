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

import json

try:
    from BaseHTTPServer import BaseHTTPRequestHandler
except ImportError:
    from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, health, *args, **kwargs):
        self.health = health
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        health_result = self.health.get_health_result()
        health_result_json = json.dumps(health_result)
        self.send_response(200 if health_result["healthy"] is True else 503)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(health_result_json.encode("utf-8")))

    def log_message(self, format, *args):
        return
