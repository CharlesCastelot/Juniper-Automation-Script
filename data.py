from pathlib import Path
import json

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

def checkPort(port):
    result = list(port)
    expected_start = "ge-0/0/"
    expected_chars = list(expected_start)
    for i in range(len(expected_chars)):
        if i >= len(result) or result[i] != expected_chars[i]:
            print(f"Invalid port format. Port should start with '{expected_start}'.")
            return False
    
    if len(result) == 7:
        print("Invalid port format. No port number provided.")
        return False

    if len(result) == 8:
        if result[7] == '*':
            return True
        if not result[7].isdigit():
            print("Invalid port format. Port number should only contain digits.")
            return False
        port_num = int(result[7])
        if port_num < 0 or port_num > 47:
            print("Invalid port number. Port should be between 0 and 47.")
            return False

    if len(result) == 9:
        if not result[7].isdigit() or not result[8].isdigit():
            print("Invalid port format. Port number should only contain digits.")
            return False
        port_num = int(result[7] + result[8])
        if port_num < 0 or port_num > 47:
            print("Invalid port number. Port should be between 0 and 47.")
            return False

    if len(result) > 9:
        print("Invalid port number. Port should be between 0 and 47.")
        return False

    return True

def checkMac(mac):
    values = mac.split(":")
    if len(values) != 6:
        print("Invalid MAC address format. Please enter in format XX:XX:XX:XX:XX:XX.")
        return False
    for val in values:
        if len(val) != 2:
            print("Invalid MAC address format. Each octet should be two hexadecimal digits.")
            return False
        try:
            int(val, 16)
        except ValueError:
            print("Invalid MAC address format. Each octet should be a valid hexadecimal number.")
            return False
    return True