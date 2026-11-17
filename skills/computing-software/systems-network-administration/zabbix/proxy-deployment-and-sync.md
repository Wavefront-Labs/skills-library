---
id: computing-software.systems-network-administration.zabbix.proxy-deployment-and-sync
name: proxy-deployment-and-sync
category: computing-software
field: systems-network-administration
product: zabbix
tags: [proxy, distributed-monitoring, proxy-buffer, config-sync, history-cache-throttling, distributed, sync]
level: practitioner
status: docs-checked
description: "Deploy a Zabbix proxy as a data collector, tune buffers and config sync, and understand server-side throttling."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/distributed_monitoring/proxies
  - https://www.zabbix.com/documentation/current/en/manual/distributed_monitoring/proxies/sync
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A proxy collects data for the server to monitor remote or unreliable locations, offload the server and simplify firewalls: it needs only one TCP connection to the server. It must use its own database; pointing it at the server database breaks the configuration.

A proxy is a data collector only. It runs items (agent, simple, trapper, SNMP and traps, IPMI, JMX, log, internal, SSH, Telnet, external, dependent, script, browser, web monitoring), preprocessing, network discovery, autoregistration, low-level discovery data collection and remote commands. It does not calculate triggers, process events, correlate or send alerts. For active agents to use the proxy, list it in ServerActive.

Data is stored locally before transmission. ProxyLocalBuffer and ProxyOfflineBuffer control how long it is kept.

In Administration > Proxies the proxy name must equal the Hostname in the proxy config file.

Configuration sync is incremental and revision-based: only modified entities are sent. Changing one item sends all configuration of that host. A full sync happens on proxy start or restart, HA failover, changed session token or failed update. ProxyConfigFrequency sets the interval (10 seconds by default). On active proxies it replaces the deprecated ConfigFrequency; using both makes the proxy log an error and terminate. The -R config_cache_reload command on the proxy starts an incremental update.

Overload protection: the server stops accepting proxy data when history cache use hits 80 percent, resumes one proxy at a time at 60, and returns to normal at 20. Watch zabbix[wcache,history,pused].

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (distributed_monitoring/proxies; distributed_monitoring/proxies/sync): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
