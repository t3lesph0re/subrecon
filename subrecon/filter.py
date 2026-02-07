#!/usr/bin/env python3
"""
Filter httpx output by HTTP status code.
"""
import re

ANSI_RE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')


def filter_by_status(input_file: str, output_file: str, statuses: set[str] = {"200"}) -> int:
    """Filter live.txt by status codes. Returns count of matching URLs."""
    kept = 0
    with open(input_file, "r", errors="ignore") as fin, open(output_file, "w") as fout:
        for line in fin:
            clean = ANSI_RE.sub("", line).strip()
            if not clean:
                continue
            if any(f"[{s}]" in clean for s in statuses):
                url = clean.split()[0]
                fout.write(url + "\n")
                kept += 1

    label = ",".join(sorted(statuses))
    print(f"[4/4] Filtered [{label}] → {kept} URL(s) → {output_file.split('/')[-1]}")
    return kept
