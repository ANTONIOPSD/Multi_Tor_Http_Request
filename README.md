# Multi_Tor_Http_Request

This is a set of scripts that allows you to run http requests from different IPs using multiple Tor relays/nodes or a combination of Tor relays/nodes and public/private socks5 proxies.

<br />

## You need to be able to:

### 1. Know how to craft custom http requests.
### 2. Understand basic Python code.

<br />
<br />

## Q/A

### What's the main purpose of this?

You can stress test your web servers (or others') by sending hundreds or thousands of packets containing custom form post requests, database searches and content loading requests.
Each request needs less than 10KB of data, but that data can make some servers crash because of the need of high CPU and RAM usage to process them.
(database search, email answering, forms etc.)



### Why 2 different scripts?

Well, **Tor IPs are public**, so anyone can download and get the full list and block them, so in case a server blocks the Tor connections,
you can run them behind a private/public proxy but... 

### "why don't you just connect through proxies directly?"

Easy answer, because proxy servers can be configured to leak your real IP, so if that happens, the web server you are trying to connect to can get the IP
of the proxy you are using as well as your real IP.

### So... how does it work?

It's very simple:
http request from your device -> Tor relay/node -> Socks5 Server -> Destination server

The script first runs multiple connections to multiple Tor relays, then each http request is sent to one of the connected relays,
then that relay sends the same requests to a public/private socks5 proxy server so that proxy server thinks that your IP is the Tor one,
then the proxy server will send the request to the destination server and in case that proxy server is misconfigured to leak your IP,
the destination server will only see the proxy server IP and the leaked Tor relay IP.


### That's it?
Nope, there is a problem, and that problem is that if you want to open connections to multiple Tor relays, **you have to run multiple Tor proccesses
and that takes a lot RAM, between 10 and 25 megabytes each one** and also a lot of CPU power if you want to run a lot of connections.

**1000 instances will use between 10 and 25 GB of RAM + the RAM the OS is using for other tasks** and probably make any mid range CPU stay at 100% **and slow
everythong down.**

The scripts are just examples so you will probably have to modify many parts of them to your needs.

## Steps:

### 1.  Donwload the latest tor-win64-0.x.x.x.zip from:
###     https://dist.torproject.org/torbrowser/
###     Example: https://dist.torproject.org/torbrowser/11.0.13/tor-win64-0.4.7.7.zip

### 2.	Extract the files like in the image:
<br />

![imagen](https://user-images.githubusercontent.com/1978099/169203804-2f36b0fe-7c73-4bdb-844d-f48e4c5c2eb8.png)

### 3.  Copy the geoip and geoip6 files inside the geoip folder

 Once you've done that, you can install all the needed python modules (tested on Windows 11, Python 3.9.12):

### pip install -r requirements.txt

<br />
<br />

## Running the scripts

First you need to edit the settings in the **config.txt**
After that you have to run the **01_Start_Tor_Instances.py** and it will create all the needed config for each Tor intance
and after that it will start all of them. **(remember the RAM usage per process, don't make you PC explode and destroy our galaxy)**

Once you have all your Tor proccesses running, you can run one of the next scripts:

## 02_Run_Request_Only_Tor.py
This script runs an http request in a loop using a different running Tor process each time

<br />

## 03_Run_Request_With_Proxies.py
This script runs an http request in a loop using a different running Tor process each time but chained with a socks5 public/private server to hide your IP
so the proxy server cannot see your real IP and leak it in case it's a malicious proxy server.




The next image is just the example included in one of the scripts, it will get the IP of each request.
<br />
![imagen](https://user-images.githubusercontent.com/1978099/169211489-e7b95b3a-ddb0-44b4-9688-298d4510dd70.png)


You can edit the that with your custom http request and you can also add multiple functions inside the main request scriptts so each relay/proxy server
can run different requests at the same time.


### The scripts are made in a quick way, so they can be optimized a lot, so feel free to copy and modify whatever you want.

## Love!

<a href="https://www.buymeacoffee.com/ANTONIOPS" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
