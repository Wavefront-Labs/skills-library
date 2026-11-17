---
id: computing-software.systems-network-administration.linux.ufw-uncomplicated-firewall
name: ufw-uncomplicated-firewall
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ufw, uncomplicated-firewall, ubuntu, debian, host-firewall, ufw-limit, app-profiles, docker-ufw, security, sysadmin]
level: practitioner
status: docs-checked
description: "Protect Ubuntu/Debian hosts with ufw: default policies, enabling without locking out SSH, allow/deny/limit by source and port, app profiles, numbered deletes, logging, and the Docker bypass."
sources:
  - https://manpages.ubuntu.com/manpages/noble/man8/ufw.8.html
  - https://help.ubuntu.com/community/UFW
  - https://wiki.ubuntu.com/UncomplicatedFirewall
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ufw — the Ubuntu host firewall

**Goal:** default-deny inbound with exactly the needed openings, enabled remotely without
losing the SSH session.

## 1. Enable safely
```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH                 # or: ufw allow from 10.0.99.0/24 to any port 22 proto tcp
ufw show added                    # rules as added on the command line, review before enabling
ufw enable                        # warns about SSH; rules persist and load at boot
ufw status verbose
```
Add the SSH rule **before** `enable`; enabling with no SSH rule drops your session.

## 2. Rules
```bash
ufw allow 443/tcp
ufw allow proto tcp from 10.0.0.0/8 to any port 5432
ufw deny from 203.0.113.45
ufw insert 1 deny from 203.0.113.0/24     # first-match: put denies above broad allows
ufw limit ssh                             # denies an IP that attempts 6 or more connections within 30 seconds
ufw allow in on eth1 to any port 53 proto udp
ufw route allow in on wg0 out on eth0     # forwarding rules; also set net/ipv4/ip_forward=1 in /etc/ufw/sysctl.conf, then ufw disable && ufw enable
ufw status numbered
ufw delete 3                              # or: ufw delete allow 443/tcp
ufw app list; ufw app info 'Nginx Full'   # profiles in /etc/ufw/applications.d/
```
Rules are evaluated in order, first match wins; `status numbered` shows that order.

## 3. Logging and files
- `ufw logging off|low|medium|high|full` (default low) → logged to the kernel log (LOG_KERN facility), possibly also `/var/log/ufw.log`.
- Custom raw rules live in the rules files under `/etc/ufw`; see `ufw-framework(8)`.
- IPv6 is enabled by default; set `IPV6=no` in `/etc/default/ufw` and reload to accept IPv6 only on loopback.

## Gotchas
- **Docker bypasses ufw**: Docker routes published container traffic in the `nat` table, so packets are diverted before they reach the INPUT and OUTPUT chains ufw uses.
  Bind published ports to `127.0.0.1` (`-p 127.0.0.1:8080:80`) to keep them host-only; Docker also provides a `DOCKER-USER` iptables chain for user rules.
- `ufw reset` disables ufw and resets it to installation defaults (`--force` skips the prompt).

## Verify
- [ ] `ufw status verbose` shows the default incoming policy and only the intended ALLOW rules (v4 and v6).
- [ ] From another host only the opened ports answer; SSH still works after reboot.

## Checked

Date: 2026-10-25. Documentation release: ufw(8) as published for Ubuntu 24.04 (manpages.ubuntu.com noble), Docker docs packet-filtering-firewalls.md, port-publishing.md and firewall-iptables.md (docker/docs main), read 2026-10-25.
Confirmed: `limit` semantics (6 connections in 30 seconds); `show added`; `route allow in on X out on Y` plus the `/etc/ufw/sysctl.conf` forwarding requirement; logging levels and default; `insert NUM`; numbered `delete`; `app list`/`app info` and `/etc/ufw/applications.d`; IPv6 default and `IPV6` in `/etc/default/ufw`; `reset`/`--force`; Docker diverting published traffic in the nat table, `127.0.0.1` publishing, and the `DOCKER-USER` chain.
Removed as unconfirmed: the `[UFW BLOCK]` prefix, before.rules/after.rules specifics and the Docker `after.rules` route, reset backup files, the iptables-nft backend statement and the firewalld/nft mixing warning.

Method: documentation only; no commands were run.
