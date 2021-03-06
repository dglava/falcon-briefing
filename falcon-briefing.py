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

import http.server
import socket
import socketserver
import os
import os.path
import sys
import threading
import winreg
import ctypes

PORT = 8000
LOCAL_IP = socket.gethostbyname(socket.gethostname())
ctypes.windll.kernel32.SetConsoleTitleW("Falcon Briefing")

def get_falcon_path():
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    try:
        key = winreg.OpenKey(reg, r"SOFTWARE\WOW6432Node\Benchmark Sims\Falcon BMS 4.35")
        return winreg.QueryValueEx(key, "baseDir")[0]
    except FileNotFoundError:
        print("Cannot find the Falcon BMS path in Windows Registry. Install broken?")
        sys.exit(1)

def remove_old_briefings(briefing_path):
    for f in os.listdir(briefing_path):
        if f.endswith(".html"):
            os.remove(os.path.join(briefing_path, f))

def run_http_server(path):
    # runs a HTTP server in the background, which serves the briefing files
    def http_server():
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        print("Briefings are served at http://{}/current-briefing.html".format(LOCAL_IP))
        httpd.serve_forever()

    os.chdir(path)
    thread = threading.Thread(target=http_server, daemon=True)
    thread.start()

def watch_briefings(briefing_path):
    # waits for new files in the directory and renames every new file
    # to "current-briefing.html", which can then be opened by a browser
    for changes in watch(briefing_path):
        for change, path in changes:
            if change == Change.added:
                os.replace(path, os.path.join(briefing_path, "current-briefing.html"))

falcon_path = get_falcon_path()
briefing_path = "{}\\User\\Briefings".format(falcon_path)

remove_old_briefings(briefing_path)
run_http_server(briefing_path)
watch_briefings(briefing_path)
