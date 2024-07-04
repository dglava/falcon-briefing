# Falcon Briefing
# Copyright (C) 2021-2024 Dino Duratović <dinomol at mail dot com>
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
    from watchfiles import watch, Change
except ImportError:
    print("Watchfiles module missing. Please install watchfiles")
    sys.exit(1)

import ctypes
import struct
import mmap
import argparse
import http.server
import socket
import socketserver
import os
import os.path
import sys
import threading
import time

class Strings():
    name = "FalconSharedMemoryAreaString"
    area_size_max = 1024 * 1024
    id = [
        "BmsExe",
        "KeyFile",
        "BmsBasedir",
        "BmsBinDirectory",
        "BmsDataDirectory",
        "BmsUIArtDirectory",
        "BmsUserDirectory",
        "BmsAcmiDirectory",
        "BmsBriefingsDirectory",
        "BmsConfigDirectory",
        "BmsLogsDirectory",
        "BmsPatchDirectory",
        "BmsPictureDirectory",
        "ThrName",
        "ThrCampaigndir",
        "ThrTerraindir",
        "ThrArtdir",
        "ThrMoviedir",
        "ThrUisounddir",
        "ThrObjectdir",
        "Thr3ddatadir",
        "ThrMisctexdir",
        "ThrSounddir",
        "ThrTacrefdir",
        "ThrSplashdir",
        "ThrCockpitdir",
        "ThrSimdatadir",
        "ThrSubtitlesdir",
        "ThrTacrefpicsdir",
        "AcName",
        "AcNCTR",
        "ButtonsFile",
        "CockpitFile",
        "NavPoint",
        "ThrTerrdatadir"
    ]

    def add(self, id, value):
        setattr(self, id, value)

def read_shared_memory_strings():
    """Reads the Falcon BMS shared memory and returns its content.

    It reads just the part of the shared memory which holds the various strings.
    Returns a String() instance with the strings as object attributes.
    """
    try:
        sm = mmap.mmap(-1, Strings.area_size_max, Strings.name, access=mmap.ACCESS_READ)
        version_num = struct.unpack('I', sm.read(4))[0]
        num_strings = struct.unpack('I', sm.read(4))[0]
        data_size = struct.unpack('I', sm.read(4))[0]
        instance = Strings()
        for id in Strings.id:
            str_id = struct.unpack('I', sm.read(4))[0]
            str_length = struct.unpack('I', sm.read(4))[0]
            str_data = sm.read(str_length + 1).decode('utf-8').rstrip('\x00')
            instance.add(id, str_data)
        sm.close()
        return instance
    except Exception as e:
        print("Error reading shared memory '{}': {}".format(Strings.name, e))
        return None

def notify(message):
    print("[Falcon-Briefing]: {}".format(message))

class SilentHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Suppress log messages of the http server."""
    def log_message(self, format, *args):
        return

def falcon_running():
    strings = read_shared_memory_strings()
    if strings.BmsBriefingsDirectory:
        return True

def read_config_file(config_file_path):
    with open(config_file_path, "r") as config_file:
        config = []
        for line in config_file:
            if line.startswith("set"):
                config.append(line.strip().split())
        return config

def verify_options(config_content):
    print_file = False
    append_briefing = False
    briefing_html = False
    for line in config_content:
        if line[1] == "g_nPrintToFile" and line[2] == "1":
            print_file = True
        elif line[1] == "g_bAppendToBriefingFile" and line[2] == "0":
            append_briefing = True
        elif line[1] == "g_bBriefHTML" and line[2] == "1":
            briefing_html = True
    return print_file & append_briefing & briefing_html

def options_are_set_in(config_content):
    for line in config_content:
        if line[1] in ["g_nPrintToFile", "g_bAppendToBriefingFile", "g_bBriefHTML"]:
            return True

def remove_old_briefings(briefing_path):
    for f in os.listdir(briefing_path):
        if f.endswith(".html"):
            os.remove(os.path.join(briefing_path, f))

def run_http_server(path, port):
    """Runs a HTTP server in the background, which serves the briefing files."""
    local_ip = socket.gethostbyname(socket.gethostname())
    def http_server():
        Handler = SilentHTTPHandler
        httpd = socketserver.TCPServer(("", port), Handler)
        notify("Briefings are served at http://{}:{}/current-briefing.html".format(local_ip, port))
        httpd.serve_forever()

    os.chdir(path)
    thread = threading.Thread(target=http_server, daemon=True)
    thread.start()

def watch_briefings(briefing_path):
    """Waits for new files in the directory and renames them.

    Practically the main loop of the utility. Watches the folder with
    the briefings for changes and renames new briefings appropriately.
    """
    for changes in watch(briefing_path):
        for change, path in changes:
            # the rename (os.replace) itself generates an event (change);
            # the "not in path" filters those out, i.e. it only works on
            # briefing files (those in xxxx-xx-xx_xxxxxx_briefing format)
            if change == Change.added and "current-briefing.html" not in path:
                os.replace(path, os.path.join(briefing_path, "current-briefing.html"))
                notify("Briefing saved — ready to be viewed")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--port",
    help="Port for the HTTP server",
    type=int,
    default=8000
    )
options = parser.parse_args()
port = options.port

ctypes.windll.kernel32.SetConsoleTitleW("Falcon Briefing")

notify("Waiting for Falcon BMS to start")
while not falcon_running():
    time.sleep(2)
notify("Falcon BMS started")

falcon_strings = read_shared_memory_strings()
falcon_config_path = r"{}\falcon bms.cfg".format(falcon_strings.BmsConfigDirectory)
user_config_path = r"{}\Falcon BMS User.cfg".format(falcon_strings.BmsConfigDirectory)
falcon_config_content = read_config_file(falcon_config_path)
user_config_content = read_config_file(user_config_path)

if verify_options(user_config_content):
    notify("All options are correctly set")
# cannot just check if the falcon config options are correct, because the user options
# take precedence and if they lack just one of the required ones, it might not work
elif verify_options(falcon_config_content) and not options_are_set_in(user_config_content):
    notify("All options are correctly set")
else:
    notify("Options are not set correctly. Please add these to your config file:")
    notify("g_bBriefHTML 1")
    notify("g_nPrintToFile 1")
    notify("g_bAppendToBriefingFile 0")
    sys.exit(1)

briefing_path = falcon_strings.BmsBriefingsDirectory
remove_old_briefings(briefing_path)
run_http_server(briefing_path, port)
watch_briefings(briefing_path)
