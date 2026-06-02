from jnpr.junos import Device
from pathlib import Path
from lxml import etree
from data import file_check
import json

def main():
    print("Welcome to the Juniper Backup Script!")
    data = file_check()
    try:
        with Device(host=data["host"], user=data["user"], password=data["password"]).open() as dev:
            print("Connected to device: " + data["host"])
            print("Backing up configuration...")
            config = dev.rpc.get_config()
            backup_file = f"{data['host']}_backup.xml"
            with open(backup_file, "w") as f:
                f.write(etree.tostring(config, pretty_print=True).decode())
            print(f"Configuration backed up to {backup_file}")
    except Exception as e:
        print(f"Failed to connect to {data['host']}: {e}")
        return


if __name__ == "__main__":
    main()
