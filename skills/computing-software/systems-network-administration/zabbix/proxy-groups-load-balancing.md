---
id: computing-software.systems-network-administration.zabbix.proxy-groups-load-balancing
name: proxy-groups-load-balancing
category: computing-software
field: systems-network-administration
product: zabbix
tags: [proxy-groups, failover, load-balancing, high-availability, serveractive, proxy, group]
level: advanced
status: docs-checked
description: "Group proxies for automatic failover and host redistribution, and configure agents to match."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/distributed_monitoring/proxies/ha
  - https://www.zabbix.com/documentation/current/en/manual/web_interface/frontend_sections/administration/proxy_groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A proxy group (Administration > Proxy groups) lets the server's proxy group manager redistribute hosts automatically. Hosts must be monitored by the group, not by single proxies; use host Mass update to move them.

Settings:
- Failover period: how long a proxy may stay silent before it is Offline (default 1m, range 10s to 15m). Its hosts are then immediately redistributed.
- Minimum number of proxies: online proxies required to keep the group online (default 1, range 1 to 1000). Keep it below the group size; in a group of 10, a minimum of 10 takes the group offline when any proxy fails. Online proxies in an offline group keep working.

Balancing: new work goes to the proxy with fewest hosts. Rebalancing begins when a proxy differs from the group average by at least 10 hosts and a factor of 2 and the imbalance lasts past a grace period of 10 times the failover period. Fewer than 10 hosts in a group may give uneven distribution.

States: Unknown, Online, Degrading, Offline, Recovering. Monitor with zabbix[proxy group,<name>,state] and zabbix[proxy group,discovery].

Agent setup:
- Passive: list all group proxies in Server.
- Active: list all group proxies or the server in ServerActive. With a single listed proxy the agent can still reach the right one.
- Only agent 7.0 or later works with proxy groups in active mode.
- The proxy's address field for active agents and senders needs a proxy group selected.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (distributed_monitoring/proxies/ha; web_interface/frontend_sections/administration/proxy_groups): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
