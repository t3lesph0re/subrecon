#!/usr/bin/env python3
"""
Remove intermediate recon files.
"""
import os

ARTIFACTS = ["subs.txt", "resolved.txt", "live.txt", "live-200.txt"]


def cleanup(directory: str = "."):
    """Remove recon artifacts from the given directory."""
    print(f"[*] Cleaning {directory}/")
    removed = 0
    for f in ARTIFACTS:
        path = os.path.join(directory, f)
        if os.path.exists(path):
            os.remove(path)
            print(f"  [-] Removed: {f}")
            removed += 1

    if removed == 0:
        print("  [*] Nothing to clean.")
    else:
        print(f"[✓] Removed {removed} file(s).")
