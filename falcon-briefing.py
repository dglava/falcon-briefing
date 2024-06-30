# Falcon Briefing
# Copyright (C) 2021-2023 Dino Duratović <dinomol at mail dot com>
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
from enum import IntEnum
import argparse
import http.server
import socket
import socketserver
import os
import os.path
import sys
import threading
import time

class StringIdentifier(IntEnum):
    BmsExe = 0
    KeyFile = 1
    BmsBasedir = 2
    BmsBinDirectory = 3
    BmsDataDirectory = 4
    BmsUIArtDirectory = 5
    BmsUserDirectory = 6
    BmsAcmiDirectory = 7
    BmsBriefingsDirectory = 8
    BmsConfigDirectory = 9
    BmsLogsDirectory = 10
    BmsPatchDirectory = 11
    BmsPictureDirectory = 12
    ThrName = 13
    ThrCampaigndir = 14
    ThrTerraindir = 15
    ThrArtdir = 16
    ThrMoviedir = 17
    ThrUisounddir = 18
    ThrObjectdir = 19
    Thr3ddatadir = 20
    ThrMisctexdir = 21
    ThrSounddir = 22
    ThrTacrefdir = 23
    ThrSplashdir = 24
    ThrCockpitdir = 25
    ThrSimdatadir = 26
    ThrSubtitlesdir = 27
    ThrTacrefpicsdir = 28
    AcName = 29
    AcNCTR = 30
    ButtonsFile = 31
    CockpitFile = 32
    NavPoint = 33
    ThrTerrdatadir = 34

class SilentHTTPHandler(http.server.SimpleHTTPRequestHandler):
    # suppres log messages of the http server
    def log_message(self, format, *args):
        return

def read_shared_memory():
    """Reads the Falcon BMS shared memory and returns its content.

    It reads just the part of the shared memory which holds the various strings.
    Returns a list of lists in the form of ((string, data), (string, data), ...
    See StringIdentifier() for the exact layout.
    """
    shm = mmap.mmap(-1, 1024 * 1024, "FalconSharedMemoryAreaString", access=mmap.ACCESS_READ)
    version_num = struct.unpack('I', shm.read(4))[0]
    num_strings = struct.unpack('I', shm.read(4))[0]
    data_size = struct.unpack('I', shm.read(4))[0]
    strings_list = []
    for _ in range(num_strings):
        str_id = struct.unpack('I', shm.read(4))[0]
        str_length = struct.unpack('I', shm.read(4))[0]
        str_data = shm.read(str_length + 1).decode('utf-8').rstrip('\x00')
        identifier = StringIdentifier(str_id).name
        strings_list.append((identifier, str_data))
    return strings_list

def wait_falcon_running():
    print("Waiting for Falcon BMS to start...")
    while True:
        strings = read_shared_memory()
        # verifies by checking if the strings are populated
        if strings and strings[9][1]:
            print("Falcon BMS started.")
            return strings
        time.sleep(1)

def get_falcon_path(strings):
    falcon_path = strings[2][1]
    return falcon_path

def get_briefing_path(strings):
    briefing_path = strings[8][1]
    return briefing_path

def verify_html_output_option(strings):
    """Verifies that the proper options are set inside Falcon BMS."""
    config_path = strings[9][1]
    config_file = open("{}\\falcon bms.cfg".format(config_path))
    for i in config_file:
        if i.strip().startswith("set g_nPrintToFile") and i.strip().endswith("0"):
            print("Option 'Briefing Output to File' is turned off - must be enabled. Exiting...")
            sys.exit(1)
        if i.strip().startswith("set g_bAppendToBriefingFile") and i.strip().endswith("1"):
            print("Option 'Append New Briefings' is turned on - must be turned off. Exiting...")
            sys.exit(1)
        if i.strip().startswith("set g_bBriefHTML") and i.strip().endswith("0"):
            print("Option 'HTML Briefings' is turned off - must be turned on. Exiting...")
            sys.exit(1)

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
        print("Briefings are served at http://{}:{}/current-briefing.html".format(local_ip, port))
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
                print("Briefing saved — ready to be viewed")

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
strings = wait_falcon_running()
verify_html_output_option(strings)
falcon_path = get_falcon_path(strings)
briefing_path = get_briefing_path(strings)
remove_old_briefings(briefing_path)
run_http_server(briefing_path, port)
watch_briefings(briefing_path)
