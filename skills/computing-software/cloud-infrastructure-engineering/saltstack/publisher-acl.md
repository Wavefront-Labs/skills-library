---
id: computing-software.cloud-infrastructure-engineering.saltstack.publisher-acl
name: publisher-acl
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, acl, publisher-acl, permissions, non-root, master-config]
level: advanced
status: docs-checked
description: "Let non-root local users run limited Salt commands via publisher_acl: matching, function and target limits, directory permissions, upgrade step."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/publisheracl.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# publisher_acl

Allows local system users other than root to run selected Salt commands from the master. Configure under `publisher_acl` in the master config; match users by exact name, shell glob or regex, and map each to allowed functions. Functions can be limited to minions and to specific args/kwargs. The page's example: one user may run anything, another only `test.*` and `pkg.*` on `web*` minions, another `my_mod.*` with argument patterns.

Permissions:
- `chmod 755` on `/var/cache/salt`, `/var/cache/salt/master`, `/var/cache/salt/master/jobs`, `/var/run/salt`, `/var/run/salt/master`.
- `/var/log/salt` and the log file must be writable by those users, or logging must be disabled.

Upgrading from an earlier version: remove old user keys (`rm /var/cache/salt/.*key`) and restart the master.

`publisher_acl` is a whitelist. `publisher_acl_blacklist` allows everything except listed operations; the page does not describe its syntax.

## Checked

2026-11-09. Read against the publisher ACL source (doc/ref/publisheracl.rst); the example, permissions, upgrade step and whitelist note were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
