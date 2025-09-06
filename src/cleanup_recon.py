#!/usr/bin/env python3
"""
File: cleanup_recon.py
Author: t3lesph0re - https://github.com/t3lesph0re
Description:
    Cleans up intermediate files:
    - Removes subs_raw.txt, subs.txt, resolved.txt, live.txt, live-200.txt
"""
import os
import sys

def cleanup(target_dir=None):
    if target_dir:
        os.chdir(target_dir)
    for f in ["subs_raw.txt", "subs.txt", "resolved.txt", "live.txt", "live-200.txt"]:
        if os.path.exists(f):
            os.remove(f)
            print(f"[🧹] Removed: {f}")
        else:
            print(f"[ ] Skipped missing: {f}")

if __name__ == "__main__":
    outdir = None
    if "--outdir" in sys.argv:
        try:
            outdir = sys.argv[sys.argv.index("--outdir") + 1]
        except (IndexError, ValueError):
            print("Error: --outdir requires a directory path")
            sys.exit(1)

    print("🧼 Cleaning up recon output files...")
    cleanup(outdir)