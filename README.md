# Falcon Briefing
Utility to show the briefing files from Falcon BMS on your smartphone,
tablet or any device running a web browser.

### How to use
1. Run either:
   * `falcon-briefing.py` with Python
   * use the precompiled executable — [see #Download](#Download)
2. Enable "Briefing Output to File" and "HTML Briefings" in the Falcon BMS options
3. Click the "Print" button when you are viewing a briefing inside Falcon BMS
4. Open the address shown in the `falcon-briefing.py` window (Example: `http://192.168.1.100:8000/current-briefing.html`)
with your smartphone's browser.

### Dependencies
* Python 3
* [Watchgod (Python module)](https://github.com/samuelcolvin/watchgod)

### Tip for Usage

I start falcon-briefing automatically whenever I open Falcon BMS (via a Windows Batch script).
After that, I created a shortcut to open the briefing (the IP address) on my smartphone's home screen.

That way all I ever have to do is start Falcon BMS, click "Print"
when I view the briefing and click on the icon on my smartphone's home screen.

### Download

Obviously it's recommended to just run the script with Python, but
you can find a compiled EXE for Windows in the [Releases](https://github.com/dglava/falcon-briefing/releases).
If you want to compile your own (see the notice below for a reason why),
you can use [PyInstaller](https://www.pyinstaller.org/).

**Notice: PyInstaller compiled Windows executables are sometimes falsely
tagged as malware by various malware tools. See [this](https://github.com/pyinstaller/pyinstaller/issues?q=is%3Aissue+virus+is%3Aclosed),
[this](https://stackoverflow.com/questions/43777106/program-made-with-pyinstaller-now-seen-as-a-trojan-horse-by-avg)
and [this](https://www.reddit.com/r/Python/comments/9ri81s/my_pyinstallercompiled_exe_progs_are_victims_of/).**

License: [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html)  
Icon used in pre-compiled EXE: [Clipboard, document icon](https://www.iconfinder.com/icons/1055091/clipboard_document_icon) by Nick Roach;
licensed under the [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html)
