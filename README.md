# Juniper Automation Scripts

PLEASE NOTE THAT THE SCRIPTS WILL STORE YOUR PASSWORD ON THE FOLDER IN PLAINTEXT RIGHT NOW. MAKE SURE TO PROTECT YOUR longinInfo.json ACCORDINGLY!

## Requirements
pip install junos-eznc lxml


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

## createVLANphone.py 
This script will setup a VOICE and DATA vlan on the switch.
Note that this code need to be ran first before setupVLANphone.py, it also only supports vlan-id from 1-254 only at the moment.

## setupVLANphone.py
This script will setup a VOICE and DATA vlan on the interface you want.
Note that it assumes you already have a VOICE and DATA vlan.

## prepareRADIUS.py
I wrote this script after making my RADIUS configurations so it's easier to remember the configuration. 
Run this and you will also have basic configs for a home RADIUS!
The configs are meant for a PEAP server with mschapv2, there is 3 retries, it uses mac-radius, and the supplicant is single (you can change to multiple or Single-Secure for security).
