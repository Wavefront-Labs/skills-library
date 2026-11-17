---
id: computing-software.systems-network-administration.zabbix.trapper-items-and-zabbix-sender
name: trapper-items-and-zabbix-sender
category: computing-software
field: systems-network-administration
product: zabbix
tags: [trapper, zabbix-sender, push-monitoring, allowed-hosts, history-push, sender, push]
level: practitioner
status: docs-checked
description: "Push values into Zabbix with trapper items and the zabbix_sender utility, including host name, key and port options."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/trapper
  - https://www.zabbix.com/documentation/current/en/manual/concepts/sender
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A trapper item accepts data instead of polling for it. Create an item of type Zabbix trapper with a key, a type of information that matches what you will send, and optionally Allowed hosts (comma-separated IPs, CIDR or DNS names; connections from other sources are refused). After saving, wait up to 60 seconds for the server's configuration cache to pick up the item before sending.

Send with the zabbix_sender command line utility:
zabbix_sender -z <server> -p 10051 -s "New host" -k trap -o "test value"
- -z server address, -p port (10051 by default).
- -s the technical host name as registered in the frontend, not the visible name.
- -k the trapper item key, -o the value.
Quote options that contain spaces with double quotes. Values can also be read from an input file, and a configuration file makes the sender use every address in ServerActive, falling back to the next if one fails.

Real-time sending groups values passed in close succession (within 0.2 seconds of the previous one, with a 1 second maximum) into one connection. Input must be UTF-8 without a byte order mark.

The sender can feed low-level discovery: the discovery rule is also a trapper item, and you pass the JSON array as the value, for example -k trapper.discovery.item -o '[{"{#FSNAME}":"/","{#FSTYPE}":"rootfs"}]'.

The server does not expand macros in the trapper key when matching. Alternatives are the Zabbix sender protocol and the history.push API method.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/trapper; concepts/sender): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
