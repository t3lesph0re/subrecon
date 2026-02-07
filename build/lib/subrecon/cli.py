#!/usr/bin/env python3
"""
CLI entry point for subrecon.

Usage:
    subrecon example.com
    subrecon example.com -o outputs/example.com
    subrecon example.com -v
    subrecon example.com --no-filter
    subrecon example.com --status 200,301,302
    subrecon clean outputs/example.com
"""
import argparse
import sys

from subrecon import __version__
from subrecon.chain import run_chain
from subrecon.filter import filter_by_status
from subrecon.cleanup import cleanup

BANNER = r"""
             __
   ___ __ __/ /  _______ _______  ___
  (_-</ // / _ \/ __/ -_) __/ _ \/ _ \
 /___/\_,_/_.__/_/  \__/\__/\___/_//_/
        t3lesph0re
"""

def main():
    # If first arg is "clean", handle it
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        directory = sys.argv[2] if len(sys.argv) > 2 else "."
        cleanup(directory)
        return

    parser = argparse.ArgumentParser(
        prog="subrecon",
        description="Subdomain recon chain: enumerate → resolve → probe → filter",
    )
    parser.add_argument("--version", action="version", version=f"subrecon {__version__}")
    parser.add_argument("domain", help="target domain")
    parser.add_argument("-o", "--outdir", help="output directory (default: ./outputs/<domain>)")
    parser.add_argument("-v", "--verbose", action="store_true", help="show tool output")
    parser.add_argument("-s", "--status", default="200", help="status codes to filter (default: 200)")
    parser.add_argument("--no-filter", action="store_true", help="skip the status code filter step")
    args = parser.parse_args()

    print(BANNER)

    outdir = args.outdir or f"outputs/{args.domain}"

    live_file = run_chain(args.domain, outdir=outdir, verbose=args.verbose)

    if not live_file:
        return

    if not args.no_filter:
        statuses = set(args.status.split(","))
        filter_by_status(f"{outdir}/live.txt", f"{outdir}/live-200.txt", statuses)

    print(f"\n[✓] Results in {outdir}/")