# Recon Scanner

A terminal-styled web UI for network port scanning and service detection.

## Features

- **4 scan modes**: Quick (top 30), Common Ports (well-known services), Full (1-10000), Custom range
- **Service detection**: Identifies common services by port + banner grabbing via TCP
- **Real-time progress**: Live progress bar, scanned/total counters, results appear as they're found
- **Dark-only UI**: GitHub Dark-inspired monospace terminal aesthetic
- **Downloadable reports**: Results saved as `.txt` files with full scan details
- **Scan history**: Browse past scans from the sidebar

## Quick Start

```bash
git clone https://github.com/sujo030902/port_scanner.git
cd port_scanner
pip install flask
python3 app.py
```

Open http://127.0.0.1:5000 in your browser.

## Usage

1. Enter a target IP or domain
2. Select scan mode (Quick, Common, Full, or Custom)
3. Click **Start Scan**
4. View open ports and banners in real-time
5. Download the report or view the dedicated results page

### Scan Modes

| Mode | Ports | Use Case |
|---|---|---|
| Quick | 1-30 | Fast check of most common ports |
| Common | Well-known services (~30 ports) | Identify popular services |
| Full | 1-10000 | Thorough scan |
| Custom | User-defined | Targeted scanning |

## Project Structure

```
├── app.py              # Flask web server
├── recon_scanner.py    # Scanning engine
├── recon.sh            # Bash launcher
├── templates/
│   ├── index.html      # Main scan interface
│   └── results.html    # Dedicated results page
└── .opencode/skills/
    └── dark-terminal-ui/SKILL.md
```

## Disclaimer

This tool is for educational purposes and authorized testing only. Only scan targets you own or have explicit permission to test.
