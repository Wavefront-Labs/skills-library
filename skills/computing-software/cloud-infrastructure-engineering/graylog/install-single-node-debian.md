---
id: computing-software.cloud-infrastructure-engineering.graylog.install-single-node-debian
name: install-single-node-debian
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [debian, ubuntu, package-install, preflight, core-model, install]
level: practitioner
status: docs-checked
description: "Install a Core Graylog cluster on Debian: MongoDB, Data Node and Graylog packages, secrets, heap, journal and preflight login."
sources:
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/debian_installation.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# install single node debian

Core cluster on Debian 12: one Graylog and MongoDB node, one separate Data Node. XFS file system strongly recommended. This guide does not configure security; secure the stack before production.

1. MongoDB: add the MongoDB apt repo, install `mongodb-org`, `apt-mark hold mongodb-org`. In `/etc/mongod.conf` set `net.bindIpAll: true` or a `bindIp` (default is local only). Enable and start `mongod.service`.
2. Data Node: install the `graylog-datanode` package from the Graylog repository package. Set `vm.max_map_count=262144`. Generate `password_secret` with `openssl rand -hex 32`. In `/etc/graylog/datanode/datanode.conf` set `password_secret`, `opensearch_heap` (half of RAM, max 31 GB; not present by default) and `mongodb_uri`. Enable and start `graylog-datanode`.
3. Graylog: install `graylog-server` (Open) or `graylog-enterprise`. In `/etc/graylog/server/server.conf` set `root_password_sha2`, the same `password_secret`, `http_bind_address`, and journal limits (recommended 72h age; size equals expected 72h volume). Set heap in `/etc/default/graylog-server` (half of RAM, max 16 GB, equal Xms and Xmx).

First login uses preflight credentials from the log file, not your root password.

## Checked

2026-11-04. Confirmed against the Debian Installation: Single Graylog Node page (Debian 12 Core cluster, XFS recommendation, security warning, MongoDB steps, vm.max_map_count, password_secret, heap advice, journal and preflight steps). Removed: the claim that the Ubuntu and RHEL guides follow the same flow (not on the page).

Method: documentation only; no commands were run.
