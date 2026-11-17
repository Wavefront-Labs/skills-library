---
id: computing-software.systems-network-administration.jellyfin.fail2ban-jellyfin-jail
name: fail2ban-jellyfin-jail
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, fail2ban, brute-force, jail, failregex, systemd-timer]
level: advanced
status: draft
description: "Ban brute-force login attempts against Jellyfin with a Fail2ban jail, filter, daily reload timer and Info-level logs."
sources: ["https://jellyfin.org/docs/general/post-install/networking/9_advanced/fail2ban/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Fail2ban for Jellyfin

Requirements: Jellyfin remotely accessible, Fail2ban running, the log location (by default `/var/log/jellyfin/` natively and `/config/log/` in Docker), and Jellyfin's log level at `Info`, because failed authentications are not logged at `Error`.

**Jail** `/etc/fail2ban/jail.d/jellyfin.local`:

```ini
[jellyfin]
backend = auto
enabled = true
port = 80,443
protocol = tcp
filter = jellyfin
maxretry = 3
bantime = 86400
findtime = 43200
logpath = /path_to_logs/log_*.log
```

Jellyfin rotates logs daily and Fail2ban does not notice the new files without a reload, so add a systemd timer (`OnCalendar=*-*-* 00:45:00`, `Persistent=true`) that runs a oneshot service `ExecStart=/usr/bin/fail2ban-client reload jellyfin`, then `sudo systemctl enable --now fail2ban-jellyfin-reload.timer`.

For Docker add `action = iptables-allports[name=jellyfin, chain=DOCKER-USER]`. For a non-standard port change `80,443` to, for example, `8096,8920`.

**Filter** `/etc/fail2ban/filter.d/jellyfin.conf`:

```ini
[Definition]
failregex = ^.*Authentication request for .* has been denied \(IP: "<ADDR>"\)\.
```

Restart Fail2ban and test with `sudo fail2ban-regex /path_to_logs/log_*.log /etc/fail2ban/filter.d/jellyfin.conf --print-all-matched`. Behind a proxy, set Known Proxies so logs hold real client IPs.
