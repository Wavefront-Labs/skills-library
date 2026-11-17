---
id: computing-software.cloud-infrastructure-engineering.graylog.mongodb-password-authentication
name: mongodb-password-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [mongodb-auth, readwrite-role, mongodb-uri, server-conf, datanode-conf]
level: advanced
status: docs-checked
description: "Switch Graylog and Data Node to an authenticated MongoDB user: roles, both config files and ordering with access control."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/configure_graylog_to_use_mongodb_password_authentication.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mongodb password authentication

Graylog connects to MongoDB as a dedicated user, separate from your admin account.

Key points:
- The user must hold the `readWrite` role in addition to any monitoring roles. Without `readWrite`, Graylog cannot read or write data and will not start.
- To show MongoDB node metrics on the Cluster Configuration page, grant the monitoring roles described in the guide.
- `server.conf` and `datanode.conf` each hold an independent `mongodb_uri`. Both must reference the same authenticated user and be updated together, or the one left unchanged cannot authenticate once access control is enforced.
- Prerequisites: MongoDB reachable from every Graylog and Data Node host, admin credentials able to create users (for example `userAdmin` or `root` on `admin`), edit access to both files on every node and permission to restart services.
- MongoDB access control (for example `security.authorization`) must be enabled, or enabled right after this change.

## Checked

2026-11-04. Confirmed against Configure Graylog to Use MongoDB Password Authentication (readWrite requirement, dbAdmin and clusterMonitor roles, prerequisites, both mongodb_uri settings updated together). Nothing removed.

Method: documentation only; no commands were run.
