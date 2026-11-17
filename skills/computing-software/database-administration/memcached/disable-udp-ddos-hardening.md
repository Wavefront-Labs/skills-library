---
id: computing-software.database-administration.memcached.disable-udp-ddos-hardening
name: disable-udp-ddos-hardening
category: computing-software
field: database-administration
product: memcached
tags: [udp, ddos, amplification, u, firewall]
level: practitioner
status: docs-checked
description: "Close the UDP amplification DDoS hole: disable UDP with -U 0 (default since 1.5.6), bind privately, and verify with netstat."
sources:
  - https://docs.memcached.org/advisories/ddos/
  - https://docs.memcached.org/serverguide/configuring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Attack: an attacker SETs a large item on an exposed server, then sends spoofed UDP GETs with the victim's IP; the server floods the victim.

Mitigation:
1. Disable UDP: add `-U 0` (default off since 1.5.6). In /etc/memcached.conf:
```
# Disable UDP protocol
-U 0
```
then restart (for example `service memcached restart`).
2. Bind to localhost or a private address: `--listen 127.0.0.1` (Debian and Ubuntu default to 127.0.0.1).
3. Firewall to block external traffic.

Verify: `sudo netstat -plunt` should show only a TCP LISTEN line for memcached (for example 127.0.0.1:11211) and no UDP socket.

Never expose memcached to the public internet.

## Checked

2026-11-04. Confirmed against the UDP DDoS advisory (attack steps, -U 0, 1.5.6 default, config file lines, netstat check, listen address, firewall) and the Configuring page. Removed: nothing.

Method: documentation only; no commands were run.
