# Parking Entry/Exit Validator

A **synthetic-data exercise** for reasoning about event matching. No real camera feeds, real license plates, or proprietary code are used.

The demo processes events in timestamp order, pairs an EXIT with the earliest unmatched ENTRY for the same exact plate, and flags orphan exits, duplicate entries, and entries remaining open. Exact matching is deliberately simplistic: real systems need to handle OCR errors, confidence scores, sites, clock drift, and operational policy.

```bash
python validator.py sample_events.csv
python -m unittest discover -s tests -v
```
