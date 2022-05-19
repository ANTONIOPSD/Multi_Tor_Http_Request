import os
import threading
import time
import random
import socket
import ctypes
import json
import pyChainedProxy as socks
import requests
from requests.structures import CaseInsensitiveDict
import requests_random_user_agent
import configparser

# Set script folder as current working folder
os.chdir(os.path.dirname(__file__))

# Prevent click on console from pausing the script (Windows only)
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.sections()
config.read("config.txt")

total_tor_instances = int(config["CONFIG"]["total_tor_instances"])
start_tor_port = int(config["CONFIG"]["start_tor_port"])
request_delay = int(config["CONFIG"]["request_delay"])
socks5_url_list = json.loads(config["CONFIG"]["socks5_url_list"])

end_tor_port = start_tor_port + ((total_tor_instances*2)-2)

def download_proxy_lists(socks5_url_list): # This shuould probably be running in a queue, but it works...
    global complete_proxy_list
    complete_proxy_list = []

    if len(socks5_url_list) > 0:
        for url in socks5_url_list:
            lista = requests.get(url, timeout=5).text.splitlines()
            for line in lista:
                complete_proxy_list.append(f"5:{line.rstrip()}")
    
    complete_proxy_list = list(dict.fromkeys(complete_proxy_list)) # Remove duplicates
    
    random.shuffle(complete_proxy_list) # Shuffle the list 

def run_request(proxy_type, ip, tor_port, proxy_port):

    # Generate a random User Agent
    random_user_agent = requests.utils.default_headers()['User-Agent'] # Just in case you need a random user agent

    # Chain of proxies, you can add more, but will be slower with each hop, the first one is one of the running Tor instances to hide your IP when sending it to the next proxy server.
    
    proxy_chain = [
    f'socks5://127.0.0.1:{tor_port}/',
    f'socks{proxy_type}://{ip}:{proxy_port}/'
    ]

    # Clear the default chain to use the next one
    socks.setdefaultproxy() 

    # Add hops with proxies
    for hop in proxy_chain:
        socks.adddefaultproxy(*socks.parseproxy(hop))
    
    # Disable proxy for localhost
    socks.setproxy('localhost', socks.PROXY_TYPE_NONE)
    socks.setproxy('127.0.0.1', socks.PROXY_TYPE_NONE)

    # Patch the socket class to run everything proxied.
    rawsocket = socket.socket
    socket.socket = socks.socksocket
    #######################################
    
    # start of custom http request

    url = "https://api.ipify.org/"
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = f"{random_user_agent}"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Connection"] = "keep-alive"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "document"
    headers["Sec-Fetch-Mode"] = "navigate"
    headers["Sec-Fetch-Site"] = "none"
    headers["Sec-Fetch-User"] = "?1"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(response.content)
    except:
        exit()  # In case of connection error, close the thread.

    #######################################

total_runs = 0

def main():
    global total_runs
    os.system("cls")
    print("Downloading proxy lists...")
    download_proxy_lists(socks5_url_list)
    print(f"Starting requests on {len(complete_proxy_list)} proxies using {total_tor_instances} Tor nodes...")
    print(f"Starting requests using {total_tor_instances} Tor nodes...")
    
    time.sleep(2)
    tor_port = start_tor_port
    
    while True:
        for line in complete_proxy_list:
            proxy = line.split(":")
            tipo = proxy[0]
            ip = proxy[1]
            proxy_port = proxy[2]
            threading.Thread(target=run_request, args=(tipo, ip, tor_port, proxy_port)).start()
            tor_port += 2
            if (tor_port >= end_tor_port):
                tor_port = start_tor_port
            time.sleep(request_delay/1000)


if __name__ == "__main__":
    main()