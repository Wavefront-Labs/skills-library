---
id: computing-software.systems-network-administration.zabbix.autoregistration-and-host-metadata
name: autoregistration-and-host-metadata
category: computing-software
field: systems-network-administration
product: zabbix
tags: [autoregistration, host-metadata, active-agent, hostmetadataitem, psk, metadata, agent]
level: practitioner
status: docs-checked
description: "Let active agents self-register, steer templates with HostMetadata, and secure registration with PSK."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/discovery/auto_registration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Active agents can register themselves: when an unknown agent asks for active checks, the server calls an action of event source Autoregistration. Network discovery is not needed. Set ServerActive in the agent config and restart it; the host is named from Hostname (or the system hostname). A comma-separated Hostname list creates a host for each name.

Configure under Alerts > Actions > Autoregistration actions. Conditions can match host name or host metadata by substring or regular expression. Operations include Add host, Add to host group, Link templates and sending messages. New hosts join Discovered hosts by default; to use another group add Remove from host group (Discovered hosts) plus Add to host group, because a host must be in a group.

If the agent has ListenIP or ListenPort, they are sent so passive checks also work; the first IP is used. Without them, the connection IP and port 10050 apply.

Host metadata comes from HostMetadata or HostMetadataItem in the agent config. HostMetadataItem can return up to 65535 UTF-8 code points, truncated beyond that. A request happens whenever the agent refreshes active checks, per RefreshActiveChecks, and immediately after restart. Registration reruns if metadata changes. The heartbeat is 120 seconds, so a deleted host is re-registered within that time.

Metadata with a secret token only gives weak protection since it is plain text. For secure registration, set PSK encryption in Administration > General > Autoregistration.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (discovery/auto_registration): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
