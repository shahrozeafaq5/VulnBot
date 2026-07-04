import os
import json
from config import SEEN_FILE


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()

    with open(SEEN_FILE, "r") as f:
        return set(json.load(f))


def save_seen(cves):
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(list(cves)), f, indent=2)