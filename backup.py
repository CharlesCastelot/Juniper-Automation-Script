from jnpr.junos import Device
from pathlib import Path
from lxml import etree
import json

def main():
    print("Welcome to the Juniper Backup Script!")
    data = file_check()
    with Device(host=data["host"], user=data["user"], password=data["password"]).open() as dev:
        print("Connected to device: " + data["host"])
        print("Backing up configuration...")
        config = dev.rpc.get_config()
        backup_file = f"{data['host']}_backup.xml"
        with open(backup_file, "w") as f:
            f.write(etree.tostring(config, pretty_print=True).decode())
        print(f"Configuration backed up to {backup_file}")

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
