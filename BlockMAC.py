from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from pathlib import Path
from data import file_check, checkMac
import json


def main():
    isValid = False
    print("Welcome to the Juniper - Block a MAC address from all ports Script!")
    data = file_check()
    try:
        with Device(host=data["host"], user=data["user"], password=data["password"], timeout=60).open() as dev:
            print("Connected to device: " + data["host"])
            while not isValid:
                mac_address = input("Enter the MAC address to block (e.g., 00:11:22:33:44:55): ")
                isValid = checkMac(mac_address)
            blockName = input("Enter a name for the block (e.g., BLOCK-1): ")
            cu = Config(dev)
            firewall_rules = f"""
            set firewall family ethernet-switching filter {blockName} term {blockName}-BLOCK from source-mac-address {mac_address}
            set firewall family ethernet-switching filter {blockName} term {blockName}-BLOCK then discard
            set firewall family ethernet-switching filter {blockName} term {blockName}-ALL then accept
            set groups {blockName} interfaces <ge-*> unit 0 family ethernet-switching filter input {blockName}
            set apply-groups {blockName}
            """

            print("Loading changes...")
            cu.load(firewall_rules, format="set")
            print(f"created object {blockName}")
            print(f"created object {blockName}-BLOCK")
            print(f"created object {blockName}-ALL")

            cu.pdiff()
            confirm = input("Apply? (yes/no): ").strip().lower()
            if confirm == "yes":
                cu.commit()
                print(f"MAC {mac_address} blocked on all ports.")
            else:
                cu.rollback()
                print("Cancelled.")
    except Exception as e:
        print(f"Failed to connect to {data['host']}: {e}")
        return

if __name__ == "__main__":
    main()
