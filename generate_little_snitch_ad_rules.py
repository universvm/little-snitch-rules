
## Read host file from Steven Black (adware + malware)

import urllib.request
import io
import re

HOST_FILE_URL = 'https://hosts-file.net/ad_servers.txt'

u = urllib.request.urlopen(HOST_FILE_URL, data = None)
f = io.TextIOWrapper(u, encoding="utf-8")
text = f.readlines()


## Parse host file --- convert to list of rules

# Only keep hostnames that follow 0.0.0.0, while removing trailing comments.
# First group is the hostname, second (optional) group is the comment.
p = re.compile("^127.0.0.1 ([^#]*)(#.*)?")

rules = []

for line in text:
  m = p.search(line)
  if m is not None:
    hostname = m.group(1).strip()
    if hostname != "127.0.0.1":
      # Append rule to block the host
      rules.append({"action":"deny", "process":"any", "remote-domains":hostname})
      
      
## Generate JSON file for little snitch

import json

OUT_FILENAME = "hphosts.lsrules"

# Create a standard JSON structure for Little Snitch
data = {}
data["name"] = "Block adware and malware"
data["description"] = "Little snitch rules to block adware and malware websites. Host lists from Steven Black."
# Add all rules
data["rules"] = rules

# Write JSON to file and download
json_data = json.dumps(data, indent=2)
with open(OUT_FILENAME, 'w+') as out_file:
  out_file.write(json_data)
