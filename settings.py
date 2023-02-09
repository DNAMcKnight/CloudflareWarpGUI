from pathlib import Path
import json

def startup():
    default = {"startupMsg": True}
    settings = Path('config.json')
    if settings.exists():
        return True
    with open('config.json', 'w') as f:
        json.dump(default, f)
    return False

