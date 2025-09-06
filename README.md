# subrecon

Tiny personal recon chain: **discover subdomains → resolve → probe → filter 200s → optional cleanup**.

## 📂 What’s included
- `src/recon_chain.py` — enumerate + probe (writes `subs_raw.txt`, `subs.txt`, `resolved.txt`, `live.txt`)
- `src/filter_200.py` — read `live.txt`, keep `[200]`, write `live-200.txt`
- `src/cleanup_recon.py` — remove intermediate files

## ⚙️ Requirements
- **Python 3.9+**
- External CLI tools (must be installed and in your `$PATH`):
  - [`assetfinder`](https://github.com/tomnomnom/assetfinder) – subdomain enumeration
  - [`dnsx`](https://github.com/projectdiscovery/dnsx) – DNS resolution
  - [`httpx`](https://github.com/projectdiscovery/httpx) – web probing

## ⏳ Install the required CLI tools

**macOS (Homebrew)**
```bash
brew install assetfinder
brew install projectdiscovery/tap/dnsx
brew install projectdiscovery/tap/httpx
```

**Linux**
Follow the instructions on each project page:
- https://github.com/tomnomnom/assetfinder
- https://github.com/projectdiscovery/dnsx
- https://github.com/projectdiscovery/httpx

**Windows**
Sorry :)

## 🚀 Quickstart

Clone the repo:

```bash
git clone https://github.com/t3lesph0re/subrecon.git
cd subrecon
```
Run the recon chain for a single domain:

```bash
python src/recon_chain.py example.com
```
Filter down to HTTP 200s:

```bash
python src/filter_200.py
```

(Optional) Clean up intermediates:

```bash
python src/cleanup_recon.py
```
Results:
- `subs.txt` → deduped subdomains
- `resolved.txt` → DNS-resolved subdomains
- `live.txt` → probed endpoints with status/title/tech
- `live-200.txt` → filtered HTTP 200s

## Usage

```bash
# Recon (quiet by default; add --verbose to stream)
python src/recon_chain.py <domain> [--outdir <dir>] [--verbose]

# Filter (default: keep 200; widen with --status)
python src/filter_200.py [--status 200,301,302,401,403] [--input <file>] [--output <file>]

# Cleanup (delete intermediate files in current folder or a specific outdir)
python src/cleanup_recon.py [--outdir <dir>]

# Examples
python src/recon_chain.py example.com --outdir outputs/example.com
python src/filter_200.py --input outputs/example.com/live.txt --output outputs/example.com/live-200.txt --status 200,301,302
python src/cleanup_recon.py --outdir outputs/example.com
```

## 🖥️ Demo
Here’s an example run against the safe test domain [`example.com`](https://example.com):

![Demo](examples/subrecon-demo.png)


## 📝 Example (one-liner helper script)

You can also use the included helper script:

```bash
./examples/quickstart.sh example.com
```

## ⚠️ Disclaimer 

Use responsibly. Only test assets you own or have explicit permission to assess.

## 📜 License

This project is licensed under the [MIT License](./LICENSE).
