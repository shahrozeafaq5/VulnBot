import json


def load_profile():
    with open("profile.json", "r") as f:
        return json.load(f)