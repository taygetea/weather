import subprocess
import sys
import time

path = sys.argv[1]
server = "taygetea@taygetea.com:"
directory = "/var/www/output/files"

filename = path.split("/")[-1]

subprocess.call(["scp", name, server + directory])
time.sleep(2)

if subprocess.check_output(["curl", "taygetea.com/files/" + filename]):
    subprocess.call(["xclip", ])
