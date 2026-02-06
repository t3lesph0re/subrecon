#!/usr/bin/env python3
"""
File: recon_chain.py
Author: t3lesph0re - https://github.com/t3lesph0re
Description:
    Subdomain recon chain:
    1. Enumerate subdomains (assetfinder + subfinder)
    2. Resolve via DNS (dnsx)
    3. Probe for web servers (httpx)

Dependencies:
    Python 3.9+, assetfinder, dnsx, httpx
    Optional: subfinder (adds more sources)

Usage:
    python3 src/recon_chain.py <domain>
    python3 src/recon_chain.py <domain> --outdir outputs/example.com
    python3 src/recon_chain.py <domain> --verbose
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

BANNER = r"""
             __
   ___ __ __/ /  _______ _______  ___
  (_-</ // / _ \/ __/ -_) __/ _ \/ _ \
 /___/\_,_/_.__/_/  \__/\__/\___/_//_/
        t3lesph0re
"""


def has_tool(name: str) -> bool:
    return shutil.which(name) is not None


def run(cmd: list[str], verbose: bool = False, capture: bool = False) -> subprocess.CompletedProcess:
    """Run a command as a list of args (no shell=True)."""
    if verbose:
        print(f"  [+] {' '.join(cmd)}")

    stdout = None if verbose and not capture else subprocess.PIPE
    stderr = None if verbose else subprocess.DEVNULL

    result = subprocess.run(cmd, stdout=stdout, stderr=stderr, text=True)

    if result.returncode != 0:
        print(f"  [!] Command failed (exit {result.returncode}): {' '.join(cmd)}", file=sys.stderr)

    return result


def enumerate_subs(domain: str, verbose: bool = False) -> set[str]:
    """Gather subdomains from available sources and dedupe."""
    subs = set()

    # assetfinder (required)
    result = run(["assetfinder", "--subs-only", domain], verbose=verbose, capture=True)
    if result.stdout:
        subs.update(line.strip() for line in result.stdout.splitlines() if line.strip())

    # subfinder (optional — adds CT logs, APIs, etc.)
    if has_tool("subfinder"):
        result = run(["subfinder", "-d", domain, "-silent"], verbose=verbose, capture=True)
        if result.stdout:
            subs.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    elif verbose:
        print("  [*] subfinder not found — skipping (install for better coverage)")

    return subs


def resolve_subs(subs_file: str, out_file: str, verbose: bool = False) -> None:
    """Resolve subdomains via dnsx."""
    run(["dnsx", "-l", subs_file, "-a", "-silent", "-o", out_file], verbose=verbose)


def probe_live(resolved_file: str, out_file: str, verbose: bool = False) -> None:
    """Probe resolved hosts for web servers via httpx."""
    run([
        "httpx", "-l", resolved_file,
        "-status-code", "-title", "-tech-detect",
        "-web-server", "-ip", "-location",
        "-silent", "-nc",
        "-o", out_file
    ], verbose=verbose)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="subrecon — subdomain recon chain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example:\n  python3 src/recon_chain.py example.com --outdir outputs/example.com --verbose"
    )
    parser.add_argument("domain", help="target domain")
    parser.add_argument("--outdir", help="output directory (default: current dir)")
    parser.add_argument("--verbose", "-v", action="store_true", help="show tool output")
    args = parser.parse_args()

    print(BANNER)

    # check required tools
    missing = [t for t in ["assetfinder", "dnsx", "httpx"] if not has_tool(t)]
    if missing:
        print(f"[!] Missing required tools: {', '.join(missing)}")
        print("    Install them and ensure they are in your $PATH.")
        sys.exit(1)

    # setup output dir
    if args.outdir:
        Path(args.outdir).mkdir(parents=True, exist_ok=True)
        os.chdir(args.outdir)

    domain = args.domain
    print(f"[*] Target: {domain}\n")

    # 1) enumerate
    print("[1/3] Enumerating subdomains...")
    subs = enumerate_subs(domain, verbose=args.verbose)
    if not subs:
        print("[!] No subdomains found. Exiting.")
        sys.exit(0)

    Path("subs.txt").write_text("\n".join(sorted(subs)) + "\n")
    print(f"      Found {len(subs)} unique subdomains → subs.txt")

    # 2) resolve
    print("[2/3] Resolving DNS...")
    resolve_subs("subs.txt", "resolved.txt", verbose=args.verbose)
    resolved_count = sum(1 for _ in open("resolved.txt")) if Path("resolved.txt").exists() else 0
    print(f"      {resolved_count} resolved → resolved.txt")

    if resolved_count == 0:
        print("[!] Nothing resolved. Exiting.")
        sys.exit(0)

    # 3) probe
    print("[3/3] Probing for live hosts...")
    probe_live("resolved.txt", "live.txt", verbose=args.verbose)
    live_count = sum(1 for _ in open("live.txt")) if Path("live.txt").exists() else 0
    print(f"      {live_count} live → live.txt")

    print(f"\n[✓] Done. Results in {os.getcwd()}")


if __name__ == "__main__":
    main()
