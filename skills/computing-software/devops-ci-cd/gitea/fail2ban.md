---
id: computing-software.devops-ci-cd.gitea.fail2ban
name: fail2ban
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-fail2ban, gitea, fail2ban-filter, iptables-allports, reverse-proxy-trusted-proxies, failed-authentication, forward-chain]
level: practitioner
status: docs-checked
description: "Ban brute-force logins on Gitea with fail2ban: log patterns, filter regex, jail settings, the Docker FORWARD jail, and real client IPs behind nginx."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/administration/fail2ban-setup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# fail2ban for Gitea

The docs warn: test it, a bad setup can lock you out. Gitea returns HTTP 200 on bad web logins, so match `log/gitea.log` instead. Lines to match: `[I] Failed authentication attempt for user from <ip>` (web/CLI), `sshConnectionFailed() [W] Failed authentication attempt from <ip>` (SSH, new in 1.15 and only logged on complete failure), `HandleText() [E] invalid credentials from <ip>`. Older `publicKeyHandler()` messages are deprecated and can be false positives because the client may still authenticate afterwards.

`/etc/fail2ban/filter.d/gitea.local`:
```ini
[Definition]
failregex =  .*(Failed authentication attempt|invalid credentials|Attempted access of unknown user).* from <HOST>
ignoreregex =
```
`/etc/fail2ban/jail.d/gitea.local`:
```ini
[gitea]
enabled = true
filter = gitea
logpath = /var/lib/gitea/log/gitea.log
maxretry = 10
findtime = 3600
bantime = 900
action = iptables-allports
```
That bans for 15 minutes on all ports after 10 failures in an hour. With Docker add `/etc/fail2ban/jail.d/gitea-docker.local` (same settings, jail `[gitea-docker]`) using `action = iptables-allports[chain="FORWARD"]`, because container traffic traverses the FORWARD chain. Apply with `service fail2ban restart`, check `service fail2ban status`.

## Real client IPs behind a proxy
Otherwise every failure shows 127.0.0.1 and you would ban the proxy. In nginx set `proxy_set_header X-Real-IP $remote_addr;` and in `app.ini` `[security]`:
```ini
REVERSE_PROXY_LIMIT = 1
REVERSE_PROXY_TRUSTED_PROXIES = 127.0.0.1/8   ; 172.17.0.0/16 for the docker default network
```

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
