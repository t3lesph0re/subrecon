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

> If you prefer other tools (e.g. `subfinder`, `amass`), update `recon_chain.py` accordingly.

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

## 🖥️ Demo
Here’s an example run against the safe test domain [`example.com`](https://example.com):

![Demo](examples/subrecon-demo.png)


## 📝 Example (one-liner helper script)

You can also use the included helper script:

```bash
./examples/quickstart.sh example.com
```

Results will be saved in the current directory:
- subs.txt → deduped subdomains
- resolved.txt → DNS-resolved subdomains
- live.txt → probed endpoints with status, title, and tech info
- live-200.txt → endpoints filtered to HTTP 200

## ⚠️ Disclaimer 

Use responsibly. Only test assets you own or have explicit permission to assess.

## 📜 License

MIT - see ./LICENSE
