# subrecon

```
             __
   ___ __ __/ /  _______ _______  ___
  (_-</ // / _ \/ __/ -_) __/ _ \/ _ \
 /___/\_,_/_.__/_/  \__/\__/\___/_//_/
        t3lesph0re
```

Subdomain recon chain: **enumerate → resolve → probe → filter**.

Takes a domain, finds subdomains from multiple sources, resolves them, probes for live web servers, and filters by status code. All output is plain text, one URL per line.

## How it works

| Step | Tool | Input | Output |
|------|------|-------|--------|
| 1. Enumerate | assetfinder + subfinder | domain | `subs.txt` |
| 2. Resolve | dnsx | `subs.txt` | `resolved.txt` |
| 3. Probe | httpx | `resolved.txt` | `live.txt` |
| 4. Filter | filter_200.py | `live.txt` | `live-200.txt` |

## Requirements

- **Python 3.9+**
- CLI tools in your `$PATH`:
  - [`assetfinder`](https://github.com/tomnomnom/assetfinder) — subdomain enum (required)
  - [`dnsx`](https://github.com/projectdiscovery/dnsx) — DNS resolution (required)
  - [`httpx`](https://github.com/projectdiscovery/httpx) — web probing (required)
  - [`subfinder`](https://github.com/projectdiscovery/subfinder) — additional enum sources (optional, recommended)

### Install tools

**macOS:**
```bash
brew install assetfinder
brew install projectdiscovery/tap/dnsx
brew install projectdiscovery/tap/httpx
brew install projectdiscovery/tap/subfinder
```

**Linux:**
```bash
go install github.com/tomnomnom/assetfinder@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

## Quickstart

```bash
git clone https://github.com/t3lesph0re/subrecon.git
cd subrecon

# Run the chain
python3 src/recon_chain.py example.com

# Filter to 200s only
python3 src/filter_200.py

# Cleanup intermediates
python3 src/cleanup_recon.py
```

## Usage

```bash
# Recon chain
python3 src/recon_chain.py <domain> [--outdir <dir>] [--verbose]

# Filter by status code
python3 src/filter_200.py [--status 200,301,302] [--input <file>] [--output <file>]

# Cleanup
python3 src/cleanup_recon.py [--outdir <dir>]
```

### Examples

```bash
# Full chain with output directory
python3 src/recon_chain.py example.com --outdir outputs/example.com --verbose

# Filter for 200s and 301s
python3 src/filter_200.py -i outputs/example.com/live.txt -o outputs/example.com/filtered.txt -s 200,301

# One-liner helper
./examples/quickstart.sh example.com
```

## Demo

![Demo](examples/subrecon-demo.png)

## Disclaimer

Use responsibly. Only test domains you own or have explicit written permission to assess.

## License

[MIT](./LICENSE)
