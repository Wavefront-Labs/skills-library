---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-fail2ban-brute-force
name: vaultwarden-fail2ban-brute-force
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, fail2ban, brute-force, jail, failregex, log-file, docker, iptables]
level: advanced
status: docs-checked
description: "Ban Vaultwarden login and admin brute force with Fail2Ban filters and jails: log requirements, failregex lines, Docker FORWARD chain, nftables and proxy IP caveats."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Fail2Ban-Setup", "https://github.com/dani-garcia/vaultwarden/wiki/Logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden with Fail2Ban

Prerequisite: log to a file (`LOG_FILE`, Vaultwarden 1.5.0+). In Docker keep `EXTENDED_LOGGING=true` (default) and use the path inside the container in `logpath`. Test with a fake account and confirm an ERROR line from `vaultwarden::api::identity` containing the IP.

Web vault filter (`filter.d/vaultwarden.local`):
```
[Definition]
failregex = ^.*?Username or password is incorrect\. Try again\. IP: <ADDR>\. Username:.*$
```
(Use `<HOST>` if an old Fail2Ban such as 0.9.7 complains of a missing host group.) Jail: `enabled = true`, `port = 80,443,8081`, `filter = vaultwarden`, `banaction = %(banaction_allports)s`, `logpath` the log file, `maxretry = 3`, `bantime = 14400`, `findtime = 14400`.

Admin page filter regex: `^.*Invalid admin token\. IP: <ADDR>.*$` with a second jail (`port = 80,443`, filter `vaultwarden-admin`).

Docker caveats: containers use the FORWARD chain, not INPUT, so set `chain = FORWARD` (Synology DSM: `DOCKER-USER`), or use `action = iptables-allports[name=vaultwarden-admin, chain=FORWARD]`. Newer Debian Fail2Ban defaults to nftables, but Docker uses iptables, so set `banaction = iptables`. Behind Cloudflare set the client IP header to `CF-Connecting-IP` in the admin panel; behind a proxy showing 127.0.0.1 in the log, forward `X-Real-IP`.

Unban: `fail2ban-client set vaultwarden unbanip 203.0.113.5` (prefix with `docker exec -t fail2ban` when containerised).

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Fail2Ban-Setup (failregex, jail settings, FORWARD/DOCKER-USER, nftables note, Cloudflare and X-Real-IP tips, unbanip).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
