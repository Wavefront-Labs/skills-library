---
id: computing-software.cloud-infrastructure-engineering.graylog.server-conf-and-file-locations
name: server-conf-and-file-locations
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [server-conf, file-locations, default-paths, datanode-conf, jvm-settings]
level: practitioner
status: docs-checked
description: "Where Graylog, Data Node, MongoDB and Forwarder config, data and logs live on DEB and RPM systems, and how server.conf relates to datanode.conf."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/default_file_locations.html
  - https://go2docs.graylog.org/current/setting_up_graylog/configuration_settings.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# server conf and file locations

Config files:
- Graylog: `/etc/graylog/server/server.conf` (logging in `log4j2.xml` beside it), journal `/var/lib/graylog-server/journal`, logs `/var/log/graylog-server`, plugins `/usr/share/graylog-server/plugin`.
- Data Node: `/etc/graylog/datanode/datanode.conf`, logs `/var/log/datanode`.
- MongoDB: `/etc/mongod.conf`, logs `/var/log/mongodb`.
- Forwarder: `/etc/graylog/forwarder/forwarder.conf`, journal `/var/lib/graylog-forwarder/data`, log `/var/log/graylog-forwarder/forwarder.log`.

Graylog server JVM settings: DEB `/etc/default/graylog-server`; RPM `/etc/sysconfig/graylog-server`. Data Node JVM settings are listed under `/etc/graylog/datanode` and Forwarder JVM options in `/etc/graylog/forwarder/jvm.options`. Data files: DEB Data Node `/var/lib/datanode/data`, MongoDB `/var/lib/mongo`; RPM `/var/lib/datanode`, `/var/lib/mongodb`.

Most `server.conf` properties rarely need changing; some must be set at install so the service starts. Some properties exist in both server.conf and datanode.conf; in multi-node setups keep shared ones consistent and per-node ones unique. Also tune MongoDB access for multiple nodes and JVM heap for Graylog, Data Node and OpenSearch. Data Node is the recommended search backend; OpenSearch 1.x is deprecated from Graylog 7.0 and to be removed in 8.0.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/setting_up_graylog/default_file_locations.html and https://go2docs.graylog.org/current/setting_up_graylog/configuration_settings.htm (both read in full, Graylog 7.2 docs).
