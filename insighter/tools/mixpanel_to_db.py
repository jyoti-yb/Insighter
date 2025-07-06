import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import pandas as pd
from collections import defaultdict
from db import insert_user_data






def convert_mixpanel_json(json_file):
    with open(json_file, 'r') as f:
        events = json.load(f)

    user_data = defaultdict(lambda: {"sessions": 0, "time_spent": 0, "clicks": 0, "actions": []})

    for e in events:
        uid = e["properties"]["distinct_id"]
        user_data[uid]["sessions"] += 1
        user_data[uid]["time_spent"] += e["properties"].get("time_spent", 0)
        user_data[uid]["clicks"] += e["properties"].get("clicks", 0)
        user_data[uid]["actions"].append(e["event"])

    rows = []
    for uid, data in user_data.items():
        converted = 1 if any(a in ["checkout", "purchase"] for a in data["actions"]) else 0
        rows.append((uid, data["sessions"], data["time_spent"], data["clicks"], converted, ";".join(data["actions"])))

    insert_user_data(rows)
    print("✅ Mixpanel JSON converted and inserted into database.")

# Example usage:
# convert_mixpanel_json('mixpanel_sample.json')
