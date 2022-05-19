import os
import sys
import subprocess

os.chdir(os.path.dirname(__file__))


subprocess.run(["Tor/tor.exe", "--hash-password", "test1234"], stderr=sys.stderr, stdout=sys.stdout)
os.system("pause")


