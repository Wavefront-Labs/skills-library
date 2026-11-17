---
id: computing-software.systems-network-administration.zabbix.server-ha-cluster
name: server-ha-cluster
category: computing-software
field: systems-network-administration
product: zabbix
tags: [high-availability, ha-cluster, hanodename, failover-delay, runtime-control, high, availability, ha]
level: advanced
status: docs-checked
description: "Run Zabbix server as an HA cluster with HANodeName, NodeAddress, failover delay and proxy and agent settings."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/concepts/server/ha
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Native Zabbix HA runs several servers as cluster nodes: one active, others standby. Switching on is non-committal and you can return to standalone at any time.

Enable it with two parameters per server, then restart:
- HANodeName: unique node identifier such as zabbix-node-01. Without it the server runs standalone.
- NodeAddress: address:port the frontend uses to reach the active node; it must match the server IP or FQDN.

Check status in Reports > System information or with zabbix_server -R ha_status.

Frontend: leave the Zabbix server address and port unset in conf/zabbix.conf.php. The frontend reads the nodes table and detects the active node.

Proxies and agents must list all nodes:
- Passive proxy: Server=zabbix-node-01,zabbix-node-02 (comma-separated).
- Active proxy: Server=zabbix-node-01;zabbix-node-02 (semicolon-separated).
- Agent passive checks: Server with commas.

Failover needs at least one standby node. If the active node shuts down and reports stopped, another takes over within 5 seconds. If it becomes unavailable without reporting, standbys wait the failover delay plus 5 seconds. The delay ranges from 10 seconds to 15 minutes, default one minute.

Runtime commands:
- zabbix_server -R ha_set_failover_delay=5m
- zabbix_server -R ha_remove_node=zabbix-node-02
Active and standby nodes cannot be removed.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (concepts/server/ha): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
