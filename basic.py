from genie.testbed import load
from genie.utils.diff import Diff
from genie.libs.ops.bgp.bgp import Bgp
import argparse
import json

#with help from 
#https://github.com/clay584/genie_collection/blob/master/clay584/genie/plugins/modules/learn_genie.py

feature = 'bgp'

parser = argparse.ArgumentParser()
parser.add_argument('action',type=str)
args = parser.parse_args()
action = args.action

host = '192.168.204.101'
port = 22
protocol = 'ssh'
username = 'fred'
password = 'bedrock'
os = 'ios'

testbed = {
    "devices": {
        host: {
            "ip": host,
            "port": port,
            "protocol": protocol,
            "username": username,
            "password": password,
            "os": os,
        }
    }
}

tb = load(testbed)
dev = tb.devices[host]
dev.connect(log_stdout=False, learn_hostname=True)
output = dev.learn(feature)

if action == 'save':
    with open('previous.txt', 'w') as f:
        f.write(json.dumps(output.info))

elif action == 'compare':
    with open('previous.txt', 'r') as f:
        previous = json.load(f)

    current = json.dumps(output.info)
    current = json.loads(current)

    exclusions = list(set().union(['bgp_neighbor_counters'], Bgp.exclude))
    dd = Diff(previous, current, exclude = exclusions)
    dd.findDiff()
    print(str(dd))
