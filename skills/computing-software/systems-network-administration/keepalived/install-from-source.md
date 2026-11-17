---
id: computing-software.systems-network-administration.keepalived.install-from-source
name: install-from-source
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, building, source-build, configure, make, dependencies, libnl, openssl]
level: practitioner
status: docs-checked
description: "Build Keepalived from a source tarball: prerequisite packages on RHEL/CentOS and Debian, then configure, make and make install."
sources:
  - https://keepalived.readthedocs.io/en/latest/installing_keepalived.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building from source

Dependencies: a compiler, OpenSSL, the Netlink library, and Net-SNMP (optional, only for SNMP).

Prerequisite packages:
- RHEL/CentOS: `yum install curl gcc openssl-devel libnl3-devel net-snmp-devel`
- Debian: `apt-get install curl gcc libssl-dev libnl-3-dev libnl-genl-3-dev libsnmp-dev`

Get the tarball from keepalived.org/download.html or the GitHub repository (acassen/keepalived). The page's example uses 1.2.15:
```
curl --progress http://keepalived.org/software/keepalived-1.2.15.tar.gz | tar xz
cd keepalived-1.2.15
./configure
make
sudo make install
```
After compiling, you still need an init script to control the daemon; the page's RHEL init-script instructions were cut off, so consult your distribution for that step.

Pass `--prefix` to configure (see the prefix skill) and `--enable-snmp` for SNMP.

Verify: the configure summary completes without missing-library errors and the installed binary reports its version.

## Checked

2026-11-04. Confirmed the dependency list, both prerequisite package commands, the download locations and the 1.2.15 example build commands on the Installing Keepalived page, and --enable-snmp on the SNMP support page. The page text for init scripts is cut off, so the skill says so. Nothing removed.

Method: documentation only; no commands were run.
