# 3meters
Ancad 3meters

New Dongle Modification:
1. copy folder /xr to /home/pi


============= New Update =================

2. cp the rc.local in /xr to /etc
3. cp the crontab to /etc
4. check if rc.local and crontab access is set to be excutable. To be safe, you can do "sudo chmod 666" to these 2 files

Test Mode
1. config_3m.py id=2019039999
2. fing the posQf=88.888 and negQf=33.333 in "def work3m()" in 3m_main.py and uncomment them. These numbers are fake number for testing. To turn to work mode, please uncomment the posQf/negQf measured by get_wq in the line above the testing ones.
3. run "sudo python3 /home/pi/3meters/3m_main.py" and check the result by the monitor or in the website

Work Mode
1. please change to the correct id in config_3m.py
2. please modify the posQf and negQf in 3m_main.py

