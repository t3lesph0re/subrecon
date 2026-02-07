#!/usr/bin/env python3
"""
Core recon chain: enumerate → resolve → probe.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def has_tool(name: str) -> bool:
    return shutil.which(name) is not None


def run(cmd: list[str], verbose: bool = False, capture: bool = False) -> subprocess.CompletedProcess:
    """Run a command as a list of args. No shell=True."""
    if verbose:
        print(f"  [+] {' '.join(cmd)}")

    stdout = None if verbose and not capture else subprocess.PIPE
    stderr = None if verbose else subprocess.DEVNULL

    result = subprocess.run(cmd, stdout=stdout, stderr=stderr, text=True)

    if result.returncode != 0 and verbose:
        print(f"  [!] Exit {result.returncode}: {' '.join(cmd)}", file=sys.stderr)

    return result


def enumerate_subs(domain: str, verbose: bool = False) -> set[str]:
    """Gather subdomains from available sources."""
    subs = set()

    # assetfinder (required)
    result = run(["assetfinder", "--subs-only", domain], verbose=verbose, capture=True)
    if result.stdout:
        subs.update(line.strip() for line in result.stdout.splitlines() if line.strip())

    # subfinder (optional)
    if has_tool("subfinder"):
        result = run(["subfinder", "-d", domain, "-silent"], verbose=verbose, capture=True)
        if result.stdout:
            subs.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    elif verbose:
        print("  [*] subfinder not found — skipping (install for better coverage)")

    return subs


def resolve_subs(subs_file: str, out_file: str, verbose: bool = False) -> None:
    run(["dnsx", "-l", subs_file, "-a", "-silent", "-o", out_file], verbose=verbose)


def probe_live(resolved_file: str, out_file: str, verbose: bool = False) -> None:
    run([
        "httpx", "-l", resolved_file,
        "-status-code", "-title", "-tech-detect",
        "-web-server", "-ip", "-location",
        "-silent", "-nc",
        "-o", out_file
    ], verbose=verbose)


def count_lines(filepath: str) -> int:
    try:
        return sum(1 for _ in open(filepath))
    except FileNotFoundError:
        return 0


def run_chain(domain: str, outdir: str = ".", verbose: bool = False) -> str | None:
    """
    Run the full chain. Returns path to live.txt or None if nothing found.
    """
    # check tools
    missing = [t for t in ["assetfinder", "dnsx", "httpx"] if not has_tool(t)]
    if missing:
        print(f"[!] Missing required tools: {', '.join(missing)}")
        print("    Install them and make sure they're in your $PATH.")
        sys.exit(1)

    Path(outdir).mkdir(parents=True, exist_ok=True)

    subs_file = f"{outdir}/subs.txt"
    resolved_file = f"{outdir}/resolved.txt"
    live_file = f"{outdir}/live.txt"

    print(f"[*] Target: {domain}\n")

    # 1) enumerate
    print("[1/3] Enumerating subdomains...")
    subs = enumerate_subs(domain, verbose=verbose)
    if not subs:
        print("[!] No subdomains found.")
        return None

    Path(subs_file).write_text("\n".join(sorted(subs)) + "\n")
    print(f"      {len(subs)} unique → subs.txt")

    # 2) resolve
    print("[2/3] Resolving DNS...")
    resolve_subs(subs_file, resolved_file, verbose=verbose)
    resolved = count_lines(resolved_file)
    print(f"      {resolved} resolved → resolved.txt")

    if resolved == 0:
        print("[!] Nothing resolved.")
        return None

    # 3) probe
    print("[3/3] Probing for live hosts...")
    probe_live(resolved_file, live_file, verbose=verbose)
    live = count_lines(live_file)
    print(f"      {live} live → live.txt")

    if live == 0:
        print("[!] No live hosts found.")
        return None

    return live_file
