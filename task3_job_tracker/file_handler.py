import os
import json

FILENAME = "applications.json"

def load_applications():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []

def save_applications(applications):
    with open(FILENAME, "w") as f:
        json.dump(applications, f, indent=4)
