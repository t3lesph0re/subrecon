#!/usr/bin/env python3
"""
File: filter_200.py
Author: t3lesph0re - https://github.com/t3lesph0re
Description:
    Filters httpx output (live.txt) by status codes.
    Default keeps only [200] responses.
    Saves results to live-200.txt (or custom output).
"""
import re
import sys

input_file = "live.txt"
output_file = "live-200.txt"
statuses = {"200"}

args = sys.argv[1:]
if "--status" in args:
    try:
        statuses = set(args[args.index("--status")+1].split(","))
    except (IndexError, ValueError):
        print("Error: --status requires a comma-separated list, e.g. 200,301,302")
        sys.exit(1)
if "--input" in args:
    try:
        input_file = args[args.index("--input")+1]
    except (IndexError, ValueError):
        print("Error: --input requires a path")
        sys.exit(1)
if "--output" in args:
    try:
        output_file = args[args.index("--output")+1]
    except (IndexError, ValueError):
        print("Error: --output requires a path")
        sys.exit(1)

ANSI_RE = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')

kept = 0
with open(input_file, "r", errors="ignore") as fin, open(output_file, "w") as fout:
    for line in fin:
        clean = ANSI_RE.sub('', line)
        if any(f"[{s}]" in clean for s in statuses):
            url = clean.strip().split()[0]
            fout.write(url + "\n")
            kept += 1

print(f"✅ Done! {kept} URL(s) with statuses {sorted(statuses)} saved to {output_file}")