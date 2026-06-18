from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from data import file_check
from data import file_check, checkPort

def main():
    isPortValid = False
    print("Welcome to the Juniper RADIUS Setup Script!")
    data = file_check()
    ServerIP = input("Enter the RADIUS server IP address: ").strip()
    secretPWD = input("Enter the RADIUS server secret password: ").strip()
    while not isPortValid:
        port_RADIUS = input("Enter the port to set 802.1X on (e.g., ge-0/0/1): ")
        isPortValid = checkPort(port_RADIUS)

    try:
        with Device(host=data["host"], user=data["user"], password=data["password"], timeout=60).open() as dev:
            print("Connected to device: " + data["host"])
            cu = Config(dev)
            print("Loading RADIUS configuration...")

            RADIUSsetup = f"""
            set access radius-server {ServerIP} secret {secretPWD}
            set access radius-server {ServerIP} port 1812
            set access radius-server {ServerIP} accounting-port 1813
            set access radius-server {ServerIP} timeout 5
            set access radius-server {ServerIP} retry 3

            set access profile DOT1X-PROFILE authentication-order radius
            set access profile DOT1X-PROFILE radius authentication-server {ServerIP}

            set protocols dot1x authenticator authentication-profile-name DOT1X-PROFILE

            set protocols dot1x authenticator interface {port_RADIUS} supplicant single
            set protocols dot1x authenticator interface {port_RADIUS} retries 3
            set protocols dot1x authenticator interface {port_RADIUS} quiet-period 60
            set protocols dot1x authenticator interface {port_RADIUS} transmit-period 30
            set protocols dot1x authenticator interface {port_RADIUS} mac-radius
            """

            cu.load(RADIUSsetup, format="set")
            cu.pdiff()
            confirm = input("Apply RADIUS configuration? (yes/no): ").strip().lower()
            if confirm == "yes":
                cu.commit()
                print("RADIUS configuration applied successfully.")

    except Exception as e:
        print(f"Failed to connect to {data['host']}: {e}")
        return


if __name__ == "__main__":
    main()
