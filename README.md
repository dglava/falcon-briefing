# Falcon Briefing ![](https://raw.githubusercontent.com/dglava/falcon-briefing/master/falcon-briefing.png)
Utility to show the briefing files from Falcon BMS on your smartphone,
tablet or any device running a web browser.

#### How to use
1. Run the `falcon-briefing.py` Python file.
2. Click the "Print" button when you are viewing a briefing inside Falcon BMS
3. Open the address shown in the `falcon-briefing.py` window (Example: `http://192.168.1.100:8000/current-briefing.html`) with your smartphone's browser.

For it to work, you have to enable the "Briefing Output to File" and
"HTML Briefings" options in Falcon BMS.

#### Dependencies
* Python 3
* [Watchgod (Python module)](https://github.com/samuelcolvin/watchgod)

#### Tip for Usage

I compiled the script into a single-file executable for use on Windows
using [PyInstaller](https://www.pyinstaller.org/). I placed the file somewhere on my disk and automatically start it whenever I open Falcon BMS. Then I also created a shortcut to the address the briefing is server at on my phone and placed it on the home screen.

That way all I ever have to do is start Falcon BMS, click on the "Print" when I view the briefing and click on the icon on my smartphone's home screen.

**Notice: PyInstaller compiled Windows executables are sometimes falsely tagged as malware by various malware tools. See [this](https://github.com/pyinstaller/pyinstaller/issues?q=is%3Aissue+virus+is%3Aclosed), [this](https://stackoverflow.com/questions/43777106/program-made-with-pyinstaller-now-seen-as-a-trojan-horse-by-avg) and [this](https://www.reddit.com/r/Python/comments/9ri81s/my_pyinstallercompiled_exe_progs_are_victims_of/).**

License: [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html)  
Icon: [Clipboard, document icon](https://www.iconfinder.com/icons/1055091/clipboard_document_icon) by Nick Roach; licensed under the [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html)
