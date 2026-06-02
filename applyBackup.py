from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from pathlib import Path
from lxml import etree
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

    
        

def file_check():
    file_path = Path("./loginInfo.json")

    if not file_path.exists():
        data = user_input()
        with open("loginInfo.json", "w") as f:
            json.dump([data], f)
        return data

    with open("loginInfo.json", "r") as f:
        sessions = json.load(f)

    if isinstance(sessions, dict):
        sessions = [sessions]
    for i in range(len(sessions)):
        if "default" in sessions[i]:
            default_idx = i
            break
    default = sessions[default_idx]
    others = [(i, s) for i, s in enumerate(sessions) if i != default_idx]

    print(f"Default: {default['host']}")
    if len(others) > 0:
        print("Other sessions:")
        for num in range(len(others)):
            print(f"  [{num + 1}] {others[num][1]['host']}")
    print("  [N] New session")
    choice = input("Select (Enter=default, number=session, N=new): ").strip()

    if choice == "":
        return default

    if choice.upper() == "N":
        data = user_input()
        for s in sessions:
            s["default"] = False
        sessions.append(data)
        with open("loginInfo.json", "w") as f:
            json.dump(sessions, f)
        return data

    try:
        num = int(choice)
        if 1 <= num <= len(others):
            orig_idx, selected = others[num - 1]
            for s in sessions:
                s["default"] = False
            sessions[orig_idx]["default"] = True
            with open("loginInfo.json", "w") as f:
                json.dump(sessions, f)
            return selected
    except ValueError:
        pass

    print("Invalid choice, using default.")
    return default


def user_input():
    data = {}
    data["host"] = input("Device IP address: ")
    data["user"] = input("Device username: ")
    data["password"] = input("Device password: ")
    data["default"] = True
    return data


if __name__ == "__main__":
    main()
