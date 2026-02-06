#!/usr/bin/env python3
"""
File: filter_200.py
Author: t3lesph0re - https://github.com/t3lesph0re
Description:
    Filters httpx output by HTTP status code.
    Default: keep 200 responses.

Usage:
    python3 src/filter_200.py
    python3 src/filter_200.py --status 200,301,302
    python3 src/filter_200.py --input outputs/example.com/live.txt --output outputs/example.com/live-200.txt
"""
import re
import sys
import argparse

ANSI_RE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')


def filter_by_status(input_file: str, output_file: str, statuses: set[str]) -> int:
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
    return kept


def main():
    parser = argparse.ArgumentParser(description="Filter httpx output by status code")
    parser.add_argument("--input", "-i", default="live.txt", help="input file (default: live.txt)")
    parser.add_argument("--output", "-o", default="live-200.txt", help="output file (default: live-200.txt)")
    parser.add_argument("--status", "-s", default="200", help="comma-separated status codes (default: 200)")
    args = parser.parse_args()

    statuses = set(args.status.split(","))
    kept = filter_by_status(args.input, args.output, statuses)
    print(f"[✓] {kept} URL(s) with status {sorted(statuses)} → {args.output}")


if __name__ == "__main__":
    main()
