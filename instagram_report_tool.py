import time
import random
import sys
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(duration, message="Processing"):
    animation = "|/-\\"
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in animation:
            sys.stdout.write(f"\r{message} {frame}")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r" + " " * len(message) + "\r", end="")

def load_proxies(proxy_type, total_proxies):
    proxies = []
    start_time = time.time()
    print(f"Loading {total_proxies} proxies of type {proxy_type}...")
    for i in range(total_proxies):
        proxy = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1000, 9999)}"
        proxies.append(proxy)
        if random.random() < 0.05:
            print(f"{i + 1}/{total_proxies} proxies loaded so far...")
        time.sleep(random.uniform(0.05, 0.15))
    print(f"All {total_proxies} proxies loaded in {round(time.time() - start_time, 2)} seconds.\n")
    return proxies

def send_reports(proxies, url, report_count, proxy_type):
    processed_reports = random.randint(int(report_count * 0.8), int(report_count * 0.95))
    total_time = random.uniform(40, 60)
    interval = total_time / processed_reports
    start_time = time.time()
    error_rate = 0.2
    errors = int(processed_reports * error_rate)
    successful_reports = processed_reports - errors
    successful_sent = 0
    error_sent = 0

    for i in range(processed_reports):
        proxy = f"@{random.choice(proxies)}"
        if error_sent < errors and random.random() < error_rate:
            sys.stdout.write(f"\r[ERROR] Failed to use {proxy_type} proxy {proxy} to report {url}... ({i + 1}/{processed_reports})")
            sys.stdout.flush()
            error_sent += 1
        else:
            sys.stdout.write(f"\rUsing {proxy_type} proxy {proxy} to report {url}... ({i + 1}/{processed_reports})")
            sys.stdout.flush()
            successful_sent += 1
        time.sleep(interval)
    
    elapsed_time = round(time.time() - start_time, 2)
    print(f"\n\nReports completed in {elapsed_time} seconds.")
    print(f"Successfully sent: {successful_sent}")
    print(f"Failed to send: {error_sent}")
    print("Please check the page.")

clear_terminal()
print("""
                                          
@@@@@@@@@@   @@@@@@@@  @@@@@@@@  @@@ @@@  
@@@@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@ @@@  
@@! @@! @@!  @@!       @@!       @@! !@@  
!@! !@! !@!  !@!       !@!       !@! @!!  
@!! !!@ @!@  @!!!:!    @!!!:!     !@!@!   
!@!   ! !@!  !!!!!:    !!!!!:      @!!!   
!!:     !!:  !!:       !!:         !!:    
:!:     :!:  :!:       :!:         :!:    
:::     ::    :: ::::   ::          ::    
 :      :    : :: ::    :           :     
                                          
Welcome to the Instagram Mass Report Tool!
This script was developed by the MefyHub Security Team for penetration testing and automation purposes. 
Contact: Telegram https://t.me/mefyhub
Contact: Telegram https://seyzalelEireli

Please note: Misuse of this tool can result in permanent bans. Use it cautiously and only for ethical testing.
Do not share this software to maintain its effectiveness and prevent blocking.
""")

url = input("Enter the Instagram profile URL: ").strip()

print("\nChoose the type of proxies:")
print("1. Mixed (HTTP, SOCKS4, SOCKS5)")
print("2. HTTP")
print("3. SOCKS4")
print("4. SOCKS5")
print("5. Residential")
proxy_choice = int(input("Enter the number corresponding to your choice: ").strip())

proxy_types = {
    1: "Mixed",
    2: "HTTP",
    3: "SOCKS4",
    4: "SOCKS5",
    5: "Residential"
}

if proxy_choice not in proxy_types:
    print("Invalid choice. Exiting.")
    sys.exit()

proxy_type = proxy_types[proxy_choice]
total_proxies = random.randint(100, 1100)

print("\nInitializing proxy loading...")
loading_animation(random.uniform(2, 5), "Initializing")
proxies = load_proxies(proxy_type, total_proxies)

report_count = int(input("\nHow many reports do you want to send? (100-10,000, recommended: 900): ").strip())
if report_count < 100 or report_count > 10000:
    print("Invalid report count. Exiting.")
    sys.exit()

print("\nProcessing...")
loading_animation(random.randint(6, 17), "Processing")

print("\nSending reports...\n")
send_reports(proxies, url, report_count, proxy_type)