---
id: computing-software.networking-hardware-and-wireless.apache-httpd.name-based-virtual-hosts
name: name-based-virtual-hosts
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, virtual-hosts, name-based, servername, serveralias, default-vhost]
level: intro
status: docs-checked
description: "Host many sites on one IP and port with name-based VirtualHost: ServerName and ServerAlias matching, the default (first-listed) host, and wildcard aliases."
sources:
  - https://httpd.apache.org/docs/2.4/vhosts/name-based.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name-based virtual hosts
Apache picks the best IP:port match first, then matches the request host name against `ServerName` and `ServerAlias` among the vhosts sharing that match. Using `*` in every `<VirtualHost>` makes IP matching irrelevant.

```apache
<VirtualHost *:80>
    # first-listed vhost is also the default for *:80
    ServerName www.example.com
    ServerAlias example.com
    DocumentRoot "/www/domain"
</VirtualHost>

<VirtualHost *:80>
    ServerName other.example.com
    DocumentRoot "/www/otherdomain"
</VirtualHost>
```

## Rules
- No match: the first-listed vhost for that IP:port serves the request.
- A request matching no `<VirtualHost>` goes to the main server config.
- Always set `ServerName` explicitly; otherwise it is inherited or found by reverse DNS, with surprising matches.
- `*` and `?` work in `ServerAlias`, e.g. `ServerAlias example.com *.example.com`. First match wins, with no precedence for wildcards or for ServerName over ServerAlias.
- Matching vhosts are processed in config order.
- Names must already resolve to the server's IP.

## Adding to an existing server
Add a default vhost whose `ServerName` matches the base server first, then add the other domains as non-default vhosts.

## Checked

2026-11-08. IP-then-name matching, default first-listed host, main-server fallback, ServerName inheritance, wildcard ServerAlias and order rules confirmed against the full name-based virtual host page.

Method: documentation only; no commands were run.
