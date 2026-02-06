#!/usr/bin/env python3
"""
File: cleanup_recon.py
Author: t3lesph0re - https://github.com/t3lesph0re
Description:
    Removes intermediate recon files.

Usage:
    python3 src/cleanup_recon.py
    python3 src/cleanup_recon.py --outdir outputs/example.com
"""
import os
import sys
import argparse

ARTIFACTS = ["subs_raw.txt", "subs.txt", "resolved.txt", "live.txt", "live-200.txt"]


def cleanup(target_dir: str | None = None):
    if target_dir:
        os.chdir(target_dir)
    removed = 0
    for f in ARTIFACTS:
        if os.path.exists(f):
            os.remove(f)
            print(f"  [-] Removed: {f}")
            removed += 1
    if removed == 0:
        print("  [*] Nothing to clean.")
    else:
        print(f"\n[✓] Removed {removed} file(s).")


def main():
    parser = argparse.ArgumentParser(description="Clean up subrecon output files")
    parser.add_argument("--outdir", help="directory to clean (default: current dir)")
    args = parser.parse_args()

    print("[*] Cleaning up...")
    cleanup(args.outdir)


if __name__ == "__main__":
    main()
