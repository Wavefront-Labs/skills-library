---
id: computing-software.networking-hardware-and-wireless.apache-httpd.ip-based-virtual-hosts-and-listen
name: ip-based-virtual-hosts-and-listen
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, virtual-hosts, ip-based, listen, multiple-daemons, ports]
level: intro
status: docs-checked
description: "Serve different sites per IP address or port with IP-based VirtualHost and Listen, and choose between multiple daemons and a single daemon."
sources:
  - https://httpd.apache.org/docs/2.4/vhosts/ip-based.html
  - https://httpd.apache.org/docs/2.4/mod/mpm_common.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP-based virtual hosts and Listen
IP-based hosting selects by the address and port a request arrives on. Each host needs a distinct IP/port combination (several NICs, IP aliases, or ports on one address).

## Listen
`Listen` is required; the server will not start without it. Duplicate pairs give `Address already in use`.
```apache
Listen 80
Listen 192.170.2.1:8443 https
```

## Option 1: multiple daemons
One httpd install per host, each with its own `Listen`, `User`, `Group`, `ServerRoot`. Use for security partitioning if you can afford memory and descriptors. httpd listens only on the wildcard or specific addresses.

## Option 2: single daemon
```apache
<VirtualHost 172.20.30.40:80>
    ServerAdmin webmaster@www1.example.com
    DocumentRoot "/www/vhosts/www1"
    ServerName www1.example.com
    ErrorLog "/www/logs/www1/error_log"
    CustomLog "/www/logs/www1/access_log" combined
</VirtualHost>
```

## Notes
- Specific IP/port beats wildcard; a matching vhost beats the base server.
- Process-creation directives cannot go in a vhost; check each Context.
- `SuexecUserGroup` is allowed if suEXEC is used.
- Use IP addresses, not hostnames, in `Listen` and `<VirtualHost>` to avoid DNS problems.
- Keep log directories unwritable by anyone but the startup user.

## Checked

2026-11-08. Listen being required, the Address already in use error for duplicate pairs, the https protocol argument, multiple-daemon vs single-daemon guidance, precedence rules, process-creation and SuexecUserGroup notes, and IP-over-hostname advice confirmed against the ip-based and mpm_common pages.

Method: documentation only; no commands were run.
