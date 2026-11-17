---
id: computing-software.systems-network-administration.zabbix.zabbix-get-troubleshooting
name: zabbix-get-troubleshooting
category: computing-software
field: systems-network-administration
product: zabbix
tags: [zabbix-get, agent-troubleshooting, tls-psk, exit-code, agent, troubleshooting]
level: practitioner
status: docs-checked
description: "Query an agent directly with zabbix_get to test keys, timeouts and PSK or certificate connections."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/concepts/get
  - https://www.zabbix.com/documentation/current/en/manual/encryption/using_pre_shared_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
zabbix_get is a command line utility that asks a Zabbix agent for one item value. It is meant for troubleshooting agents, from the server, proxy or any host allowed by the agent's Server setting.

Examples:
zabbix_get -s 127.0.0.1 -p 10050 -k system.cpu.load[all,avg1]
zabbix_get -s 192.168.1.1 -k "web.page.regexp[www.example.com,,,\"USA: ([a-zA-Z0-9.-]+)\",,\1]"

Options: -s host name or IP, -p port (default 10050), -I source address, -k item key, -t timeout in seconds (range 1-600, default 30), -P protocol with auto (default, JSON with fallback to plaintext), json, or plaintext (for 6.4.x and older agents). An unsupported key returns exit code 1.

Remember the shell strips the outer quotes, so they are not part of the key sent to the agent.

Testing an encrypted agent (PSK file readable only by the zabbix user):
zabbix_get -s 127.0.0.1 -k "system.cpu.load[all,avg1]" --tls-connect=psk --tls-psk-identity="PSK 001" --tls-psk-file=/path/to/agent.psk

Use it to separate agent problems from server problems. If zabbix_get works from the server host but the item is unsupported, check the interface address, firewall, TLS settings in the host Encryption tab, and AllowKey or DenyKey rules. If it times out, compare the timeout with the item's configured timeout.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (concepts/get; encryption/using_pre_shared_keys): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
