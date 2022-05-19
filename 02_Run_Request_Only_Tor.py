import os
import threading
import time
import ctypes
import requests
from requests.structures import CaseInsensitiveDict
import requests_random_user_agent
import configparser

# Set script folder as current working folder
os.chdir(os.path.dirname(__file__))

# Prevent click on console from pausing the script (Windows only)
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)


# Loads config from file
config = configparser.ConfigParser(inline_comment_prefixes="#")
config.sections()
config.read("config.txt")

total_tor_instances = int(config["CONFIG"]["total_tor_instances"])
start_tor_port = int(config["CONFIG"]["start_tor_port"])
request_delay = int(config["CONFIG"]["request_delay"])


end_tor_port = start_tor_port + ((total_tor_instances*2)-2)


def run_request(tor_port):

    # Create a request session and set the tor instance as proxy.
    session = requests.session()
    session.proxies = {}
    session.proxies['http']=f'socks5h://localhost:{tor_port}'
    session.proxies['https']=f'socks5h://localhost:{tor_port}'

    # Generate a random User Agent
    random_user_agent = requests.utils.default_headers()['User-Agent'] # Just in case you need a random user agent

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
        response = session.get(url, headers=headers, timeout=10)
        print(response.content)
    except:
        exit()  # Exit thread In case of connection error.

    #######################################

def main():
    tor_port = start_tor_port
    while True:
        threading.Thread(target=run_request, args=(tor_port,)).start()
        tor_port += 2
        if (tor_port >= end_tor_port):
            tor_port = start_tor_port
        time.sleep(request_delay/1000)

if __name__ == "__main__":
    main()