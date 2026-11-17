---
id: computing-software.systems-network-administration.zabbix.active-vs-passive-checks
name: active-vs-passive-checks
category: computing-software
field: systems-network-administration
product: zabbix
tags: [active-checks, passive-checks, agent, serveractive, json-protocol, active, passive, checks]
level: intro
status: docs-checked
description: "Understand how passive and active agent checks work, who initiates them, and which settings and item types each needs."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/appendix/items/activepassive
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/zabbix_agent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Passive: the server or proxy opens a TCP connection and asks for one item. Since version 7.0 the request is JSON, for example {"request":"passive checks","data":[{"key":"agent.ping","timeout":3}]}. The agent replies with version, variant (1 for agent, 2 for agent 2) and data holding either value or error. Passive checks run asynchronously: the number of async agent pollers is StartAgentPollers and concurrency per poller is capped by MaxConcurrentChecksPerPoller (1000). The agent needs Server set to accept these connections.

Active: the agent initiates. It asks the addresses in ServerActive for its check list, runs the items on its own schedule and pushes values back. Since 6.4 the list is synced incrementally every RefreshActiveChecks seconds (default 5); the full configuration is sent only when something changed. If a refresh fails it retries after a fixed 60 seconds. Active mode needs Hostname to match the frontend host.

In the frontend, choose item type Zabbix agent for passive and Zabbix agent (active) for active. Log monitoring (log, logrt) must be active.

To have an agent talk to a proxy rather than the server, list the proxy, not the server, in ServerActive. Active mode suits agents behind firewalls that block inbound connections; passive suits agents you want to poll on demand with zabbix_get.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (appendix/items/activepassive; config/items/itemtypes/zabbix_agent): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
