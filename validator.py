"""Minimal parking event validator for synthetic event data."""
import csv
import json
import sys
from collections import defaultdict, deque
from datetime import datetime


def validate(events):
    active = defaultdict(deque)
    paired, anomalies = [], []
    ordered = sorted(events, key=lambda row: datetime.fromisoformat(row["timestamp"]))
    for row in ordered:
        plate = row["plate"].strip().upper()
        kind = row["event"].strip().upper()
        if kind == "ENTRY":
            if active[plate]:
                anomalies.append({"type": "duplicate_entry", "plate": plate, "timestamp": row["timestamp"]})
            active[plate].append(row["timestamp"])
        elif kind == "EXIT":
            if active[plate]:
                paired.append({"plate": plate, "entry": active[plate].popleft(), "exit": row["timestamp"]})
            else:
                anomalies.append({"type": "orphan_exit", "plate": plate, "timestamp": row["timestamp"]})
        else:
            anomalies.append({"type": "unknown_event", "plate": plate, "timestamp": row["timestamp"]})
    for plate, timestamps in active.items():
        for stamp in timestamps:
            anomalies.append({"type": "unmatched_entry", "plate": plate, "timestamp": stamp})
    return {"paired": paired, "anomalies": anomalies}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python validator.py sample_events.csv")
    with open(sys.argv[1], newline="", encoding="utf-8") as handle:
        print(json.dumps(validate(list(csv.DictReader(handle))), indent=2))


if __name__ == "__main__":
    main()
