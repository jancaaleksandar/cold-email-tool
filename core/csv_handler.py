import csv
from csv import DictReader
from typing import Any


def read_csv(path : str) -> list[dict[str | Any, str | Any]]:
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(path : str, rows) -> None:
    if not rows:
        return

    with open(path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
