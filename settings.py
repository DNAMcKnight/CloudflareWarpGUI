from pathlib import Path
import json, sys, traceback

default = {
    "startupMsg": True,
    "winWarningMsg": True,
    "defaultTaskbar": False,
    "autoConnect": False,
    "keepAlive": False
}
def startup() -> bool:
    settings = Path(f'config.json')
    if settings.exists():
        return True
    with open('config.json', 'w') as f:
        json.dump(default, f, indent=2)
    return False

def change(key: str, value: bool) -> bool:
    with open(f"config.json", "r") as f:
        data = json.load(f)
        with open(f"config.json", "w") as write:
            data[key] = value
            json.dump(data, write, indent=2)
            return True
    return False

def check(key: str) -> bool:
    try:
        with open(f"config.json", "r") as f:
            data = json.load(f)
            if key in data:
                if data[key] != True and data[key] != False:
                    print("returning default")
                    return default[key]
                return data[key]
            return None
    except json.decoder.JSONDecodeError:
        print("decode error")
        return default[key]
        
        
        
    
print(check('startupMsg'))