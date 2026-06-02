from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from pathlib import Path
from data import file_check, checkPort
import json


def main():
    isPortValid = False
    print("Welcome to the Juniper - Voice VLAN Phone Setup Script!")
    data = file_check()
    try:
        with Device(host=data["host"], user=data["user"], password=data["password"], timeout=60).open() as dev:
            print("Connected to device: " + data["host"])
            
            while not isPortValid:
                port_vlan = input("Enter the port to to set Vlan (e.g., ge-0/0/1): ")
                isPortValid = checkPort(port_vlan)
            
            

            cu = Config(dev)
            data_vlan="DATA"
            voice_vlan="VOICE"

            phoneVlan_rules = f"""
            set interfaces {port_vlan} unit 0 family ethernet-switching port-mode access
            set interfaces {port_vlan} unit 0 family ethernet-switching vlan members {data_vlan}
            set ethernet-switching-options voip interface {port_vlan} vlan {voice_vlan}
            set poe interface {port_vlan}
            """

            print("Loading changes...")
            cu.load(phoneVlan_rules, format="set")

            cu.pdiff()
            confirm = input("Apply? (yes/no): ").strip().lower()
            if confirm == "yes":
                cu.commit()
                print(f"Vlan applied to {port_vlan}.")
            else:
                cu.rollback()
                print("Cancelled.")
    except Exception as e:
        print(f"Failed to connect to {data['host']}: {e}")
        return

if __name__ == "__main__":
    main()