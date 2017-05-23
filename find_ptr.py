#!/usr/bin/env python

from dns import reversename
from dns import resolver
from sys import argv
import re
import ipaddress

# IPv4 net, that passed to script as argument
net = ipaddress.ip_network(unicode((argv[1:2])[0]), strict=False)

# RegEXP for find PTR
regexp = re.compile("(?P<PTR>\S+\.)")

for ip in net:

	domain_address = reversename.from_address(str(ip))
	domain_name = str(resolver.query(domain_address,"PTR")[:])
	match = regexp.findall(domain_name)
	
	if "unallocated" not in match[0]:
		print "\n{} has PTR:\n    {}".format(ip, match)
