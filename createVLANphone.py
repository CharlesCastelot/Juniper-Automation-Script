from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from data import file_check
from data import file_check, checkPort

def main():
    isPortValid = False
    print("Welcome to the Juniper VLAN Setup Script!")
    data = file_check()
    vlanNamePhone = input("Enter the name for the phone VLAN (default: VOICE): ").strip()
    if not vlanNamePhone:
        vlanNamePhone = "VOICE"
    vlanPhoneID = input("Enter the VLAN ID for the phone VLAN (between 1-254 for now) (default: 100): ").strip()
    if not vlanPhoneID:
        vlanPhoneID = "100"
    vlanNameComputers = input("Enter the name for the computer VLAN (default: DATA): ").strip()
    if not vlanNameComputers:
        vlanNameComputers = "DATA"
    vlanComputerID = input("Enter the VLAN ID for the computer VLAN (between 1-254 for now) (default: 200): ").strip()
    if not vlanComputerID:
        vlanComputerID = "200"
    
    while not isPortValid:
        port_VLAN = input("Enter the port to set VLAN on (e.g., ge-0/0/1): ")
        isPortValid = checkPort(port_VLAN)
    try:
        with Device(host=data["host"], user=data["user"], password=data["password"], timeout=60).open() as dev:
            print("Connected to device: " + data["host"])
            cu = Config(dev)
            print("Loading VLAN configuration...")

            phoneVlan_setup= f"""
            set vlans {vlanNameComputers} vlan-id {vlanComputerID}
            set vlans {vlanNamePhone} vlan-id {vlanPhoneID}

            set interfaces ge-0/0/1 unit 0 family ethernet-switching port-mode access
            set interfaces ge-0/0/1 unit 0 family ethernet-switching vlan members {vlanNameComputers}

            set ethernet-switching-options voip interface ge-0/0/1 vlan {vlanNamePhone}

            set protocols lldp interface all
            set protocols lldp-med interface all

            set interfaces vlan unit {vlanPhoneID} family inet address 192.168.{vlanPhoneID}.1/24
            set interfaces vlan unit {vlanComputerID} family inet address 192.168.{vlanComputerID}.1/24

            set vlans {vlanNamePhone} l3-interface vlan.{vlanPhoneID}
            set vlans {vlanNameComputers} l3-interface vlan.{vlanComputerID}

            set system services dhcp pool 192.168.{vlanPhoneID}.0/24 address-range low 192.168.{vlanPhoneID}.10 high 192.168.{vlanPhoneID}.100
            set system services dhcp pool 192.168.{vlanPhoneID}.0/24 router 192.168.{vlanPhoneID}.1

            set system services dhcp pool 192.168.{vlanNameComputers}.0/24 address-range low 192.168.{vlanNameComputers}.10 high 192.168.{vlanNameComputers}.100
            set system services dhcp pool 192.168.{vlanNameComputers}.0/24 router 192.168.{vlanNameComputers}.1
            """
            print(f"The DHCP pool for the VOICE VLAN is set to 192.168.{vlanPhoneID}.0/24 with the router at 192.168.{vlanPhoneID}.1")
            print(f"The DHCP pool for the DATA VLAN is set to 192.168.{vlanNameComputers}.0/24 with the router at 192.168.{vlanNameComputers}.1")

            cu.load(phoneVlan_setup, format="set")
            cu.pdiff()
            confirm = input("Apply VLAN configuration? (yes/no): ").strip().lower()
            if confirm == "yes":
                cu.commit()
                print("VLAN configuration applied successfully.")
    except Exception as e:
        print(f"Failed to connect to {data['host']}: {e}")
        return




if __name__ == "__main__":
    main()
