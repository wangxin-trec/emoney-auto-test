@ECHO OFF
::%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d %~dp0
pip3 install -r requirements.txt
python MongoDB_health_check_per_second.py
pause