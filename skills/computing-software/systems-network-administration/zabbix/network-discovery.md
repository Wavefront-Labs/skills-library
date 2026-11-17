---
id: computing-software.systems-network-administration.zabbix.network-discovery
name: network-discovery
category: computing-software
field: systems-network-administration
product: zabbix
tags: [network-discovery, discovery-events, ip-range, discovery-actions, discovered-hosts-group, network, discovery, ip]
level: practitioner
status: docs-checked
description: "Scan IP ranges and services, understand discovery events, and avoid recreating deleted hosts."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/discovery/network_discovery
  - https://www.zabbix.com/documentation/current/en/manual/discovery/network_discovery/rule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Network discovery scans IP ranges for services and agents, then runs actions on the resulting events. It does not discover network topology.

Rule (Data collection > Discovery): name, discovered by Server or a Proxy, IP range, update interval, concurrency and checks.
- IP range formats: single address, 192.168.1-10.1-255, a mask such as 192.168.4.0/24 (/16-/30 for IPv4, /112-/128 for IPv6) or a comma-separated list. Total addresses must be under 64K.
- The interval is measured after the previous run ends, so runs never overlap.
- Checks: SSH, LDAP, SMTP, FTP, HTTP, HTTPS, POP, NNTP, IMAP, TCP, Telnet, Zabbix agent (unencrypted queries only), SNMPv1/2/3 and ICMP ping. Ports can be a single value, range or list.
- SNMPv3 checks run on one worker. Queue limit is about 2000000 checks or 4 GB; if full the rule is skipped with a log warning. Monitor with the zabbix[discovery_queue] internal item.

Events: Service Discovered, Up, Lost, Down, and Host Discovered, Up, Lost, Down.

Actions can add or remove hosts, enable or disable them, add or remove groups and tags, link templates and run remote scripts. Because actions fire for any event, add the condition Discovery status: up, otherwise a manually deleted host that is offline raises Service Lost and is recreated next cycle.

Created hosts go to the Discovered hosts group by default. Linking templates fails collectively if any have clashing unique entities such as the same item key.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (discovery/network_discovery; discovery/network_discovery/rule): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
