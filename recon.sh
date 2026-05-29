#!/usr/bin/env bash

BOLD='\033[1m'
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CYAN='\033[94m'
MAGENTA='\033[95m'
RESET='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_SCRIPT="$SCRIPT_DIR/app.py"

check_deps() {
    PYTHON="python3"
    if ! command -v python3 &>/dev/null; then
        PYTHON="python"
    fi

    if ! $PYTHON -c "import flask" 2>/dev/null; then
        echo -e "${RED}[!] Flask is not installed. Installing...${RESET}"
        pip3 install --break-system-packages flask 2>/dev/null || pip3 install --user flask 2>/dev/null
    fi
}

check_deps

echo -e "${CYAN}${BOLD}"
echo "   ____                       ____"
echo "  / __ \___  ___ ___  ___   / __/__  ___________"
echo " / /_/ / _ \/ -_) _ \/ _ \ / _// _ \/ __/ __/ -_)"
echo " \____/ .__/\__/_//_/ .__//_/  \___/_/  \__/\__/"
echo "     /_/           /_/"
echo -e "${GREEN}${BOLD}     Recon Scanner - Web UI${RESET}"
echo -e "${RESET}"
echo -e "${MAGENTA}  [!] This tool performs network scanning.${RESET}"
echo -e "${MAGENTA}  [!] Only use on targets you own or have permission to test.${RESET}"
echo -e "${RESET}"

read -p "$(echo -e "${YELLOW}[?] Press Enter to launch web interface or Ctrl+C to exit...${RESET}")"

echo -e "${GREEN}[+] Starting web server...${RESET}"
$PYTHON "$APP_SCRIPT"
