from pathlib import Path
import json, sys

def startup():
    default = {
    "startupMsg": True,
    "winWarningMsg": True,
    "defaultTaskbar": False,
    "autoConnect": False,
    "keepAlive": False
}
    settings = Path(f'config.json')
    if settings.exists():
        return True
    with open('config.json', 'w') as f:
        json.dump(default, f, indent=2)
    return False

def change(key, value):
    with open(f"config.json", "r") as f:
        data = json.load(f)
        with open(f"config.json", "w") as write:
            data[key] = value
            json.dump(data, write, indent=2)
            return True
    return False

def check(key):
    with open(f"config.json", "r") as f:
        data = json.load(f)
        if key in data:
            return data[key]
        return None