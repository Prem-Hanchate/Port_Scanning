# Quick Start Guide

## 🚀 Run the Scanner in 3 Steps

### Step 1: Make Bash Script Executable (Linux/Mac Only)
```bash
chmod +x advanced_port_scan.sh
```

### Step 2: Run the Python Controller
```bash
python port_scanner.py
```

### Step 3: Enter Your Scan Details
- **Target**: IP address, domain, or network (e.g., `192.168.1.1` or `scanme.nmap.org`)
- **Ports**: Port range or specific ports (e.g., `1-1024` or `80,443,8080`)

## 📌 Common Scan Examples

### Scan Local Machine
```
Target: 127.0.0.1
Ports: 1-1024
```

### Scan Web Server Ports
```
Target: example.com
Ports: 80,443,8080,8443
```

### Scan Local Network
```
Target: 192.168.1.0/24
Ports: 22,80,443
```

### Scan All Common Ports
```
Target: 192.168.1.100
Ports: 1-1024
```

## ⚠️ Important

1. **Need Admin Rights**: Run with `sudo` on Linux/Mac or as Administrator on Windows
2. **Legal Notice**: Only scan systems you own or have permission to test
3. **Install Nmap**: Make sure Nmap is installed (`nmap --version` to check)

## 🆘 Having Issues?

### On Windows:
- Install WSL: `wsl --install` in PowerShell (as Admin)
- OR install Git Bash from https://git-scm.com/

### Nmap Not Found:
- **Linux**: `sudo apt-get install nmap`
- **Mac**: `brew install nmap`
- **Windows**: Install in WSL or download from https://nmap.org/

### Script Won't Run:
- Make sure you're in the project directory
- Check Python version: `python --version` (need 3.6+)
- Try `python3` instead of `python`

---

**That's it! Happy scanning! 🎯**
