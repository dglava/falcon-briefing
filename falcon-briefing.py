# Falcon Briefing
# Copyright (C) 2021 Dino Duratović <dinomol at mail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    from watchgod import watch, Change
except ImportError:
    print("Watchgod module missing. Please install watchgod")
    sys.exit(1)

import platform
os_name = platform.system()
if os_name == "Windows":
    import winreg
    import ctypes

import argparse
import http.server
import socket
import socketserver
import os
import os.path
import sys
import threading

class SilentHTTPHandler(http.server.SimpleHTTPRequestHandler):
    # suppres log messages of the http server
    def log_message(self, format, *args):
        return

def get_falcon_path():
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    try:
        key = winreg.OpenKey(reg, r"SOFTWARE\WOW6432Node\Benchmark Sims\Falcon BMS 4.35")
        return winreg.QueryValueEx(key, "baseDir")[0]
    except FileNotFoundError:
        print("Cannot find the Falcon BMS path in the Windows Registry. Install broken?")
        input("Press any key to close")
        sys.exit(1)

def remove_old_briefings(briefing_path):
    for f in os.listdir(briefing_path):
        if f.endswith(".html"):
            os.remove(os.path.join(briefing_path, f))

def run_http_server(path, port):
    # runs a HTTP server in the background, which serves the briefing files
    local_ip = socket.gethostbyname(socket.gethostname())
    def http_server():
        Handler = SilentHTTPHandler
        httpd = socketserver.TCPServer(("", port), Handler)
        print("Briefings are served at http://{}:{}/current-briefing.html".format(local_ip, port))
        httpd.serve_forever()

    os.chdir(path)
    thread = threading.Thread(target=http_server, daemon=True)
    thread.start()

def watch_briefings(briefing_path):
    # waits for new files in the directory and renames every new file
    # to "current-briefing.html", which can then be opened by a browser
    for changes in watch(briefing_path):
        for change, path in changes:
            # the rename (replace) itself generates an event (change);
            # the "not in path" filters those out, i.e. it only works on
            # briefing files (those in xxxx-xx-xx_xxxxxx_briefing format)
            if change == Change.added and "current-briefing.html" not in path:
                os.replace(path, os.path.join(briefing_path, "current-briefing.html"))
                print("Briefing saved — ready to be viewed")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-b", "--briefings",
    help="Path of the briefing directory. Usually in Falcon BMS\\User\\Briefings",
    metavar="FOLDER"
    )
parser.add_argument(
    "-p", "--port",
    help="Port for the HTTP server",
    type=int,
    default=8000
    )
options = parser.parse_args()
port = options.port
briefing_path = options.briefings

if os_name == "Linux":
    if not briefing_path:
        print("Please specify the briefing directory. See --help")
        sys.exit(1)
elif os_name == "Windows":
    ctypes.windll.kernel32.SetConsoleTitleW("Falcon Briefing")
    if not briefing_path:
        falcon_path = get_falcon_path()
        briefing_path = "{}\\User\\Briefings".format(falcon_path)

remove_old_briefings(briefing_path)
run_http_server(briefing_path, port)
watch_briefings(briefing_path)
