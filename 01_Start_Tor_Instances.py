import threading
import subprocess
import os
import ctypes
import time
import time
import shutil
import configparser

os.chdir(os.path.dirname(__file__))
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.sections()
config.read("config.txt")

total_tor_instances = int(config["CONFIG"]["total_tor_instances"])
start_tor_port = int(config["CONFIG"]["start_tor_port"])
ExcludeNodes = config["CONFIG"]["ExcludeNodes"]
HashedControlPassword = config["CONFIG"]["HashedControlPassword"]

def kill_current_tor_instances():
    print("Closing all current Tor proccesses")
    os.system("taskkill.exe /im tor.exe /F")
    time.sleep(2)
    os.system("cls")

def create_config():
    if os.path.exists("Tor/config"):
        for file in os.listdir("Tor/config"):
            os.remove(os.path.join("Tor/config", file))
    time.sleep(1)
    config_number = 1
    end_tor_port = start_tor_port + (total_tor_instances * 2)
    for tor_port in range(start_tor_port, end_tor_port, 2):
        if not os.path.exists("Tor/config"):
            os.makedirs("Tor/config")
        if os.path.exists(f'Tor/config/tor_config_{config_number}'):
            os.remove(f'Tor/config/tor_config_{config_number}')
        config_file = open(f'Tor/config/tor_config_{config_number}', 'a')
        config_text = f'GeoIPFile Tor/geoip/geoip\nGeoIPv6File Tor/geoip/geoip6\nSOCKSPort {tor_port}\nDataDirectory Tor/data/tor_data_{config_number}\nControlPort {tor_port + 1}\nHashedControlPassword {HashedControlPassword} \nCookieAuthentication 1\nExcludeNodes {ExcludeNodes}\nStrictNodes 1'
        config_file.write(f'{config_text}\n')
        config_file.close()
        if not os.path.exists(f'Tor/data/tor_data_{config_number}'):
            os.makedirs(f'Tor/data/tor_data_{config_number}')
        config_number = config_number + 1

def initial_instance():
    print("Killing all current Tor instances...")
    os.system("taskkill.exe /im tor.exe /F")
    os.system("cls")
    print("Killing all current Tor instances...")
    print("Starting first instance and replicating cache...")

    process = subprocess.Popen(f"Tor/tor.exe -f Tor/config/tor_config_1", stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline().decode('utf-8')
        if "Bootstrapped 100%" in output:
            time.sleep(2)
            break
    os.system("taskkill.exe /im tor.exe /F")
    print("First Tor instance started successfully")
    time.sleep(1)
    print("Copying cache to the rest of instances...")
    for instance in range(2, total_tor_instances + 1):
        if not os.path.exists(f'Tor/data/tor_data_{instance}/cached-certs'):
            if os.path.exists(f'Tor/data/tor_data_1/cached-certs'):
                shutil.copy("Tor/data/tor_data_1/cached-certs", f"Tor/data/tor_data_{instance}/cached-certs")
        
        if not os.path.exists(f'Tor/data/tor_data_{instance}/cached-microdesc-consensus'):
            if os.path.exists(f'Tor/data/tor_data_1/cached-microdesc-consensus'):
                shutil.copy("Tor/data/tor_data_1/cached-microdesc-consensus", f"Tor/data/tor_data_{instance}/cached-microdesc-consensus")

        if not os.path.exists(f'Tor/data/tor_data_{instance}/cached-microdescs'):
            if os.path.exists(f'Tor/data/tor_data_1/cached-microdescs'):
                shutil.copy("Tor/data/tor_data_1/cached-microdescs", f"Tor/data/tor_data_{instance}/cached-microdescs")
        
        if not os.path.exists(f'Tor/data/tor_data_{instance}/cached-microdescs.new'):
            if os.path.exists(f'Tor/data/tor_data_1/cached-microdescs.new'):
                shutil.copy("Tor/data/tor_data_1/cached-microdescs.new", f"Tor/data/tor_data_{instance}/cached-microdescs.new")
    time.sleep(1)

def start_instance(current_instance):
    process = subprocess.Popen(f"Tor/tor.exe -f Tor/config/tor_config_{current_instance}", stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode('utf-8')
        if "Bootstrapped 100%" in output:
            completed_instance_list.append(current_instance)
            break
  
def check_started_instances():
    previous_instances = len(completed_instance_list)
    while True:
        completed_instances = len(completed_instance_list)
        if (completed_instances != previous_instances):
            print(f"Started: {completed_instances} of {total_tor_instances} Tor instances.")
            previous_instances = completed_instances
        if (completed_instances >= total_tor_instances):
            print(f"All {total_tor_instances} instances started succesfully.")
            print("Now you can start the second script")
            print("Don't close this window, it will kill all Tor proccesses.")
            break

###########################################

completed_instance_list = []
current_instance = 1
create_config()
initial_instance()
threading.Thread(target=check_started_instances).start()
print(f"Starting and checking {total_tor_instances} Tor instances...")
while (current_instance <= total_tor_instances):
    threading.Thread(target=start_instance, args=(current_instance,)).start()
    time.sleep(0.01)

    current_instance += 1

