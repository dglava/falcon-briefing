# Falcon Briefing
Utility to show the briefing files from Falcon BMS on your smartphone,
tablet or any device running a web browser.

### How to use
1. Enable "Briefing Output to File" and "HTML Briefings" in the Falcon BMS options
2. Run `falcon-briefing.py` with Python
3. Click the "Print" button when you are viewing a briefing inside Falcon BMS
4. Open the address shown in the `falcon-briefing.py` window (Example: `http://localhost:8000/current-briefing.html`)
with your smartphone's browser.

### Dependencies
* Python 3
* [Watchgod (Python module)](https://github.com/samuelcolvin/watchgod)

### Tip for Usage

You can create a Windows batch file to automatically start falcon-briefing
together with Falcon BMS. Then create a shortcut for the address the briefing is
being served at on your phone's homescreen. That way you just have to press
"Print" in the briefing screen and click the shortcut on your phone's homescreen.

Pre-compiled EXE files for Windows were hosted on Github, but I decided
to remove them. They were always flagged as malware by most security software
(see [this](https://github.com/pyinstaller/pyinstaller/issues?q=is%3Aissue+virus+is%3Aclosed),
[this](https://stackoverflow.com/questions/43777106/program-made-with-pyinstaller-now-seen-as-a-trojan-horse-by-avg)
and [this](https://www.reddit.com/r/Python/comments/9ri81s/my_pyinstallercompiled_exe_progs_are_victims_of/)).
If you still need them for some reason, you can compile it yourself with PyInstaller.

License: [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html)  
