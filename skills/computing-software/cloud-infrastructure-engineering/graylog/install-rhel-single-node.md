---
id: computing-software.cloud-infrastructure-engineering.graylog.install-rhel-single-node
name: install-rhel-single-node
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [rhel, rpm, almalinux, rocky-linux, package-install, install]
level: practitioner
status: docs-checked
description: "Install a Core Graylog cluster on Red Hat 8 or 9: prerequisites, the service files to adjust and where JVM settings live on RPM systems."
sources:
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/red_hat_installation.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/default_file_locations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# install rhel single node

The Red Hat guide covers Red Hat 8 or 9 and derivatives with a Core cluster: one Graylog and MongoDB node and one Data Node. It installs the same three services as the Debian guide: MongoDB, Graylog Data Node, Graylog.

Prerequisites: required ports open, XFS strongly recommended, review the Core architecture. The guide does not configure security settings.

RPM default locations differ from DEB:
- Graylog JVM settings: `/etc/sysconfig/graylog-server` (DEB: `/etc/default/graylog-server`).
- Data Node data: `/var/lib/datanode`.
- MongoDB data: `/var/lib/mongodb`.

Shared across both: `/etc/graylog/server/server.conf`, `/etc/graylog/datanode/datanode.conf`, `/etc/mongod.conf`, journal `/var/lib/graylog-server/journal`, logs under `/var/log/graylog-server`, `/var/log/datanode`, `/var/log/mongodb`.

Page inconsistency: the guide says to open the graylog-server file found by default at `/etc/graylog/` but then edits `/etc/sysconfig/graylog-server`.

Set the Graylog `password_secret` identically on Graylog and Data Node nodes, as for any platform.

## Checked

2026-11-04. Confirmed against the Red Hat install guide. Page inconsistency recorded: it says to open the graylog-server file under /etc/graylog/ but then edits /etc/sysconfig/graylog-server.

Method: documentation only; no commands were run.
