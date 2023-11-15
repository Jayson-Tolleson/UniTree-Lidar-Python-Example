import subprocess
from subprocess import Popen, PIPE, STDOUT, run
C = ('./unilidar_publisher_udp &')
subprocess.run(C, shell=True, stderr=subprocess.STDOUT)
python = ('sudo nohup python3 console.py &')
subprocess.run(python, shell=True, stderr=subprocess.STDOUT)


