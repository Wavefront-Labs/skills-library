---
id: computing-software.networking-hardware-and-wireless.kea.starting-kea-dhcp4-and-config-testing
name: starting-kea-dhcp4-and-config-testing
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, command-line, config-test, startup]
level: intro
status: docs-checked
description: "Start kea-dhcp4 directly or via keactrl, use the -c, -d, -t and -T switches, test a configuration file, and read the exit code."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# starting kea-dhcp4 and testing configuration
The docs recommend starting and stopping Kea with keactrl, but kea-dhcp4 can be run directly. Switches:

- `-c file`: configuration file; the only mandatory switch.
- `-d`: debug mode. Severity and debuglevel in the file are ignored; "debug" and the maximum level (99) apply.
- `-t file`: load, check and exit. Exit code 0 means OK, 1 means an error. The check is not comprehensive.
- `-T file`: load and check with extra checks: opens database connections (lease, host, config backend, forensic logging), loads hook libraries and parses their configuration. It does not open sockets, lock files or open or rotate files, so it will not interfere with a running process on the same machine.
- `-v` prints the version and exits.
- `-p` and `-P` change the server and client UDP ports; only useful for testing, since a server on non-standard ports cannot serve normal DHCPv4 queries.

Both test switches print log messages to standard output and errors to standard error.

## Checked

2026-11-08. Read the DHCPv4 server chapter section 'Starting and Stopping the DHCPv4 Server' in full: the recommendation to use keactrl, and the -c, -d, -t, -T, -v, -p and -P switch descriptions, exit codes and the -T extra checks. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
