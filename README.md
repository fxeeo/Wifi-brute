<h1 align="center">
  <br>
  WIFI-Brute-Force V2.0
  </h1>

### Description
A Wi-Fi Brute Force tool that automatically scans for available networks and attempts to crack them using provided wordlists.

### Features
- **Auto-Scanning**: Automatically detects available Wi-Fi networks.
- **Auto-Wordlist**: Automatically fetches wordlists from the `wordlist` folder.
- **Auto-Install**: Automatically installs required dependencies (`pywifi`).
- **Interactive UI**: Real-time status updates with color-coded results.

### Installation & Usage

1. Clone or download the repository.
2. Ensure you have Python installed.
3. Run the script:
   ```bash
   python3 WifiBF.py
   ```
4. The script will:
   - Check if Wi-Fi is enabled.
   - Scan for networks.
   - Load wordlists from the `wordlist` directory (or prompt if empty).
   - Start attempting to crack detected networks.

### Requirements
- Python 3.x
- Wi-Fi adapter (Built-in or External)

### Note
This tool is for educational purposes only. Do not use it on networks you do not own or have permission to test.
