---
id: computing-software.networking-hardware-and-wireless.opnsense.alias-hosts-networks-ports-mac
name: alias-hosts-networks-ports-mac
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [aliases, host-alias, network-alias, port-alias, mac-alias]
level: practitioner
status: docs-checked
description: "How host, network, port and MAC aliases accept values in OPNsense: FQDN resolve interval, exclusions, wildcard masks, port ranges and ARP/NDP-based MAC matching."
sources: ["https://docs.opnsense.org/manual/aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Host, network, port and MAC aliases

Host aliases accept a single IP, a range separated by a minus sign, or a fully qualified domain name. FQDNs are re-resolved periodically; the default is every 300 seconds. To change that, go to Firewall > Settings > Advanced and set Aliases Resolve Interval to the number of seconds. After applying, open Firewall > Diagnostics > Aliases and pick the alias to see the resolved addresses (a name such as a video site may resolve to many IPs).

Hosts and Networks aliases can hold exclusions: an entry starting with "!" (for example !192.168.0.0/24) removes that host or network from the alias or from a Network group that includes it. Pf tables support these exceptions natively.

Networks use CIDR notation; /32 is one IPv4 host, /128 one IPv6 host, /24 equals 255.255.255.0 and /64 is a normal IPv6 LAN. A wildcard mask also works, so 192.168.0.1/0.0.255.0 matches every address ending in .1 across the 192.168.X.1 networks.

Ports are single numbers or a range with a colon, e.g. 20:25.

MAC aliases take a full or partial hex address (f4:90:ea matches a vendor prefix, f4:90:ea:00:00:01 a single device). They are resolved on a periodic schedule from the arp and ndp tables, so the contents can lag reality. MAC addresses can be spoofed, so filtering on them is no more secure than filtering on IP addresses.

Warning: the Flush action on an alias is not persistent. It empties the current contents, which repopulate for non-external types, so it rarely helps. If an alias is used by a rule with state tracking, existing states may need to be removed (Firewall > Diagnostics > States Dump) before new contents take effect.

## Checked

2026-11-03. Read the Aliases manual page (aliases.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
