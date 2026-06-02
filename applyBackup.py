from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from pathlib import Path
from lxml import etree
from data import file_check
import json

def main():
    print("Welcome to the Juniper Backup Applying Script!")
    backup_file = input("Place the xml is the same folder as the script and enter the  XML file name (e.g. 192.168.1.1_backup.xml): ").strip()
    if not Path(f"./{backup_file}").exists():
        print(f"File '{backup_file}' not found.")
        return
    data = file_check()
    with Device(host=data["host"], user=data["user"], password=data["password"], timeout=60).open() as dev:
        print("Connected to device: " + data["host"])
        with Config(dev, mode="exclusive") as cu:
            print("Loading backup configuration...")
            cu.load(path=backup_file, format="xml", overwrite=True)
            print("\n--- Configuration diff ---")
            diff = cu.diff()
            if diff is None:
                print("No differences found. Device already has this configuration.")
                cu.rollback()
            else:
                print(diff)
                confirm = input("\nApply this configuration? (yes/no): ").strip().lower()
                if confirm == "yes" or confirm == "y":
                    cu.commit(timeout=120)
                    print("Configuration applied successfully.")
                else:
                    cu.rollback()
                    print("Cancelled. No changes made.")

    
        



if __name__ == "__main__":
    main()
