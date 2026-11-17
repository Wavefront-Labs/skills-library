---
id: computing-software.systems-network-administration.keepalived.install-from-repositories
name: install-from-repositories
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, installing, packages, yum, apt-get, rhel, debian]
level: intro
status: docs-checked
description: "Install Keepalived from distribution repositories on Red Hat or Debian with yum or apt-get, and the trade-off that packaged versions lag the latest stable release."
sources:
  - https://keepalived.readthedocs.io/en/latest/installing_keepalived.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing from distribution repositories

The fastest route, but the packaged version is typically a few releases behind the latest stable version. Compile from source if you need the newest release.

- **Red Hat Enterprise Linux:** Keepalived has been in the base repository since Red Hat 6.4.
  `yum install keepalived` (dependencies come with it).
- **Debian:** `apt-get install keepalived`.

Source-build dependencies, for comparison: a compiler, OpenSSL, the Netlink library, and optionally Net-SNMP (only for SNMP support).

## Checked

2026-11-04: repository versions lag, Red Hat 6.4 base repository, yum and apt-get commands and source-build dependencies confirmed against the Installing Keepalived page. Removed the Verify line.
Method: documentation only; no commands were run.
