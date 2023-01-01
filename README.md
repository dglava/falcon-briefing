# Falcon Briefing
Utility to show the briefing files from Falcon BMS on your smartphone,
tablet or any device running a web browser.

### How to use
1. Enable "Briefing Output to File" and "HTML Briefings" in the Falcon BMS options
2. Run `falcon-briefing.py` with Python
3. Click the "Print" button when you are viewing a briefing inside Falcon BMS
4. Open the address shown in the `falcon-briefing.py` window (Example: `http://192.168.1.100:8000/current-briefing.html`)
with your smartphone's browser.

### Dependencies
* Python 3
* [Watchfiles (Python module)](https://github.com/samuelcolvin/watchfiles)

### Tip for Usage
For ultimate convenience, as with my other [utility which randomizes the cockpit switches at startup](https://github.com/dglava/falcon-bcc),
it is recommended to add it to a startup script, which would start it
together with Falcon BMS. Also consider creating a shortcut to the address the briefing
is being server at on your phone's homescreen. That way you just have to press "Print"
in the briefing screen and click the shortcut on your phone's homescreen.

License: [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html)  
