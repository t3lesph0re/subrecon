#!/usr/bin/env python3
"""
File: recon_chain.py
Author: t3lesph0re - https://github.com/t3lesph0re
Description:
    Runs a simple subdomain recon chain:
    - Enumerates subdomains (assetfinder)
    - Resolves them (dnsx)
    - Probes for web servers (httpx)
    - Saves results to subs.txt, resolved.txt, live.txt

Dependencies:
    - Python 3.9+
    - assetfinder
    - dnsx
    - httpx

Usage:
    python src/recon_chain.py <domain>
    python src/recon_chain.py <domain> --outdir outputs/example.com
    python src/recon_chain.py <domain> --verbose
    python src/recon_chain.py <domain> --outdir outputs/example.com --verbose
"""
import os
import sys
import shlex
import subprocess

def run_cmd(cmd: str):
    print(f"\n[+] Running: {cmd}")
    proc = subprocess.run(cmd, shell=True)
    if proc.returncode != 0:
        print(f"[!] Command failed (exit {proc.returncode}): {cmd}", file=sys.stderr)
        sys.exit(proc.returncode)

def main(domain: str, outdir: str | None = None, verbose: bool = False):
    # optional output directory
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        os.chdir(outdir)

    print(f"\n🔎 Starting recon for: {domain}")
    qdomain = shlex.quote(domain)

    # 1) Subdomain enumeration (assetfinder)
    if verbose:
        # show findings live while also saving them
        run_cmd(f"assetfinder --subs-only {qdomain} | tee subs_raw.txt")
        run_cmd(f"sort -u subs_raw.txt | tee subs.txt > /dev/null")
    else:
        run_cmd(f"assetfinder --subs-only {qdomain} > subs_raw.txt 2>/dev/null")
        run_cmd("sort -u subs_raw.txt > subs.txt 2>/dev/null")

    # 2) DNS resolution (dnsx)
    if verbose:
        # write file; let stdout show progress if the tool prints any
        run_cmd("dnsx -l subs.txt -a -silent -o resolved.txt")
    else:
        run_cmd("dnsx -l subs.txt -a -silent -o resolved.txt > /dev/null 2>&1")

    # 3) Web server probing (httpx) — disable ANSI with -nc
    httpx_cmd = (
        "httpx -l resolved.txt -status-code -title -tech-detect "
        "-web-server -ip -location -silent -nc -o live.txt"
    )
    if verbose:
        run_cmd(httpx_cmd)  # stream output if any
    else:
        run_cmd(f"{httpx_cmd} > /dev/null 2>&1")

    print("\n✅ Recon complete!")
    print("🔹 Subdomains: subs.txt")
    print("🔹 Resolved:   resolved.txt")
    print("🔹 Live:       live.txt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/recon_chain.py <domain> [--outdir <dir>] [--verbose]")
        sys.exit(1)

    domain = sys.argv[1]
    outdir = None
    verbose = False

    if "--outdir" in sys.argv:
        try:
            outdir = sys.argv[sys.argv.index("--outdir") + 1]
        except (IndexError, ValueError):
            print("Error: --outdir requires a directory path")
            sys.exit(1)

    if "--verbose" in sys.argv:
        verbose = True

    main(domain, outdir, verbose)