# Juniper Automation Scripts

I currently have 5 automation scripts:

1. Backup.py
2. applyBackup.py
3. BlockMAC.py
4. BlockMAC_AllBut1Port.py
5. setupVLANphone.py


## Backup.py
This script creates and saves a backupfile named <host-IP>_backup.xml.
Keep this file around to you can return to a previous backup.
Note: The file will be re-written if you don't change the name on the next run.


## applyBackup.py
This script pairs with the Backup.py above. 
When you have a .xml file, you can apply it with this script to apply backups.

## BlockMAC.py
Give a MAC address when prompted and it will be blocked from every interface on that switch.


## BlockMAC_AllBut1Port.py
Give a MAC address and an interface when prompted and that MAC address will be blocked from every interface except from the one you gave.

## setupVLANphone.py
This script will setup a VOICE and DATA vlan on the interface you want.
Note that it assumes you already have a VOICE and DATA vlan. More scripts comming soon!