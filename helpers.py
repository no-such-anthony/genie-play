# no-such-anthony
# https://github.com/no-such-anthony/genie-play

from genie.libs.sdk.apis.utils import get_config_dict
from genie.utils import Dq

with open("switch.cfg", "r") as f:
     raw_output = f.read()

# get_config_dict stores config as keys in dict
config_dict = get_config_dict(raw_output)
config_dq = Dq(config_dict)

# svi interfaces with ip helper-address
intfs = set([x.path[0] for x in config_dq.contains('^interface Vlan.*', regex=True).contains('^ip helper-address.*',regex=True)])
print(f"Interfaces with helpers\n{intfs}\n")

# svi interfaces without ip helper-address
all_intfs = set([x.path[0] for x in config_dq.contains('^interface Vlan.*', regex=True)])
intfs_without_helpers = all_intfs.difference(intfs)
print(f"Interfaces without helpers\n{intfs_without_helpers}\n")

# unique helper-addresses over all svi interfaces
helpers = [k[18:] for k in set([x.path[1] for x in config_dq.contains('^interface Vlan.*', regex=True).contains('^ip helper-address.*',regex=True)])]
print(f"Unique helpers\n{helpers}\n")

# helper-address per interface
print('Helpers per interface')
for i in intfs:
	print(i, [k[18:] for k in config_dict[i] if k.startswith('ip helper-address')])
print()

# Another way to get helper-address per interface without dq.  Just loop through config_dict keys
print('Helpers per interface')
for i in config_dict:
    if i.startswith('interface Vlan'):
        i_helpers = [k[18:] for k in config_dict[i] if k.startswith('ip helper-address')]
        if i_helpers:
            print(i,i_helpers)
print()
