---
id: computing-software.database-administration.clickhouse.network-ports-and-firewall
name: network-ports-and-firewall
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, ports, 8123, 9000, 9009, firewall, tls]
level: practitioner
status: docs-checked
description: "ClickHouse default network ports to plan in firewalls: HTTP, native, interserver, Keeper, and their TLS variants."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/sre/network-ports.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# network ports and firewall
Ports described as default are configured in `/etc/clickhouse-server/config.xml`; customise by adding a file to `/etc/clickhouse-server/config.d/`. Default ports from the reference table:
- 8123 HTTP, 8443 HTTP SSL/TLS (the only one of these two listed for ClickHouse Cloud as well as open source)
- 9000 native protocol (clickhouse-server, clickhouse-client, native tools; also inter-server communication for distributed queries), 9440 native protocol SSL/TLS
- 9009 inter-server communication for low-level data access (data exchange, replication), 9010 SSL/TLS for inter-server communication
- 9181 recommended ClickHouse Keeper port, 9281 recommended secure Keeper port, 9234 recommended Keeper Raft port (also secure when `<secure>1</secure>` is enabled); 2181 is the ZooKeeper default (see 9181 for Keeper)
- 9004 MySQL emulation, 9005 PostgreSQL emulation (also used for secure communication if SSL is enabled), 9011 native protocol PROXYv1, 9019 JDBC bridge, 9100 gRPC, 9363 Prometheus metrics, 42000 Graphite

Open only the ports for the interfaces you actually use. Because the ports are configurable, check the effective config rather than assuming defaults.

## Checked
2026-11-03. Confirmed every port above against the "Network ports" reference table. Removed: the 8123/9000 exposure principles, the claim that Keeper ports can disrupt replication, the named config keys (`http_port`, `tcp_port`, `interserver_http_port`) and the nc/curl Verify step, none of which are on the page.
Method: documentation only; no commands were run.
