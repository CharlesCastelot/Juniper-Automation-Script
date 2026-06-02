from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from pathlib import Path
from data import file_check, checkMac, checkPortAllbut1
import json


def main():
    isMacValid = False
    isPortValid = False
    print("Welcome to the Juniper - Block a MAC address from all ports but one Script!")
    data = file_check()
    try:
        with Device(host=data["host"], user=data["user"], password=data["password"], timeout=60).open() as dev:
            print("Connected to device: " + data["host"])
            while not isMacValid:
                mac_address = input("Enter the MAC address to block (e.g., 00:11:22:33:44:55): ")
                isMacValid = checkMac(mac_address)
            
            while not isPortValid:
                port_exempt = input("Enter the port to exempt (e.g., ge-0/0/1): ")
                isPortValid = checkPortAllbut1(port_exempt)
            blockName = input("Enter a name for the block (e.g., BLOCK-1): ")
            cu = Config(dev)
            firewall_rules = f"""
            set firewall family ethernet-switching filter {blockName} term {blockName}-EXEMPT from source-mac-address {mac_address}
            set firewall family ethernet-switching filter {blockName} term {blockName}-EXEMPT from interface {port_exempt}.0
            set firewall family ethernet-switching filter {blockName} term {blockName}-EXEMPT then accept
            set firewall family ethernet-switching filter {blockName} term {blockName}-BLOCK from source-mac-address {mac_address}
            set firewall family ethernet-switching filter {blockName} term {blockName}-BLOCK then discard
            set firewall family ethernet-switching filter {blockName} term {blockName}-ALL then accept
            set groups {blockName} interfaces <ge-*> unit 0 family ethernet-switching filter input {blockName}
            set apply-groups {blockName}
            """
            print("Loading changes...")
            cu.load(firewall_rules, format="set")
            print(f"created object {blockName}")
            print(f"created object {blockName}-EXEMPT")
            print(f"created object {blockName}-BLOCK")
            print(f"created object {blockName}-ALL")

            cu.pdiff()
            confirm = input("Apply? (yes/no): ").strip().lower()
            if confirm == "yes":
                cu.commit(timeout=120)
                print(f"MAC {mac_address} blocked on all ports.")
            else:
                cu.rollback()
                print("Cancelled.")
    except Exception as e:
        print(f"Failed to connect to {data['host']}: {e}")
        return







if __name__ == "__main__":
    main()
