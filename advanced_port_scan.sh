#!/bin/bash

# Advanced Port Scanning Tool - Bash Scanner Engine
# This script performs the actual Nmap scanning operations

# Check if target and ports are provided as arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <target> <ports> [output_file]"
    exit 1
fi

target=$1
ports=$2
output_file=${3:-"scan_temp_output.txt"}

echo "[+] Bash Scanner Started" >&2
echo "[+] Target: $target" >&2
echo "[+] Ports: $ports" >&2

# ------------------ REPORT HEADER ------------------
{
echo "=============================="
echo "ADVANCED NETWORK SCAN REPORT"
echo "=============================="
echo "Target        : $target"
echo "Port Range    : $ports"
echo "Scan Time     : $(date)"
echo "Scanner       : Nmap (Bash Script)"
echo ""
} > "$output_file"

# ------------------ HOST DISCOVERY ------------------
echo "[+] Performing Host Discovery..." >&2
{
echo "-----------------------------"
echo "HOST DISCOVERY (ACTIVE HOSTS)"
echo "-----------------------------"
nmap -sn "$target" 2>&1
echo ""
} >> "$output_file"

# ------------------ OS DETECTION ------------------
echo "[+] Performing OS Detection..." >&2
{
echo "-----------------------------"
echo "OS DETECTION"
echo "-----------------------------"
nmap -O "$target" 2>&1
echo ""
} >> "$output_file"

# ------------------ PORT + SERVICE + VERSION ------------------
echo "[+] Scanning Ports, Services & Versions..." >&2
{
echo "----------------------------------------"
echo "OPEN PORTS | SERVICES | VERSION DETAILS"
echo "----------------------------------------"
nmap -sS -sV -p "$ports" -T4 "$target" 2>&1
echo ""
} >> "$output_file"

# ------------------ COMPLETION ------------------
{
echo "============================"
echo "SCAN COMPLETED SUCCESSFULLY"
echo "End Time: $(date)"
echo "============================"
} >> "$output_file"

echo "[✔] Bash Scanner Completed" >&2
echo "[✔] Raw output saved to: $output_file" >&2

exit 0
