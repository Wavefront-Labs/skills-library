---
id: computing-software.cybersecurity-defensive.network-defence.squid-proxy-filtering
name: squid-proxy-filtering
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [squid, forward-proxy, acl-filtering, ssl-bump, web-filtering, proxy-authentication, egress-control]
level: practitioner
status: docs-checked
description: "Run Squid as a filtering forward proxy: ACL design, domain and category blocklists, authentication, SSL-Bump peek-and-splice for SNI filtering, logging and egress enforcement."
sources: ["https://wiki.squid-cache.org/", "https://www.squid-cache.org/Doc/config/", "https://wiki.squid-cache.org/Features/SslPeekAndSplice"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Squid proxy filtering

## Core config (squid.conf)
```
acl localnet src 10.0.0.0/8
acl SSL_ports port 443
acl Safe_ports port 80 443
acl CONNECT method CONNECT
acl blocked_domains dstdomain "/etc/squid/blocked_domains.txt"   # .example.bad (leading dot = subdomains)
acl allowed_servers_dst dstdomain "/etc/squid/server_allow.txt"
acl servers src 10.20.0.0/16

http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access deny blocked_domains
http_access allow servers allowed_servers_dst      # servers: allow-list only
http_access deny servers
http_access allow localnet
http_access deny all
```
Order matters: first match wins.

## HTTPS filtering without full decryption (peek and splice)
```
http_port 3128 ssl-bump cert=/etc/squid/bump.pem generate-host-certificates=on
acl step1 at_step SslBump1
acl blocked_sni ssl::server_name "/etc/squid/blocked_domains.txt"
ssl_bump peek step1
ssl_bump terminate blocked_sni
ssl_bump splice all
```
This reads SNI and blocks without decrypting allowed traffic. Full bumping (decrypt) requires deploying
the proxy CA to clients and exclusions for pinned apps, banking and health sites.

## Authentication
Use `auth_param` with an authentication helper for user attribution (see the Squid configuration reference).

## Category lists
For category or reputation lists, use an external ACL helper fed by a domain list.

## Enforcement
Firewall must block direct outbound 80/443 from clients/servers, or the proxy is optional. Use WPAD/PAC
or explicit proxy via GPO/MDM.

## Logging
Log user, URL and status in `access.log`; ship to SIEM.

## Verify
- [ ] A blocked domain returns 403 or the TLS connection is terminated.
- [ ] Direct egress (bypassing proxy) fails at the firewall.

## Checked

2026-10-28. Confirmed against: Squid configuration reference (acl, http_access, auth_param, ssl_bump, at_step, ssl::server_name); Squid SslPeekAndSplice wiki page (peek at step1, terminate, splice).

Removed as unconfirmed: Kerberos helper name and proxy_auth line, SquidGuard/ufdbGuard, SNI logformat code, squid -k parse.

Method: documentation only; no commands were run.
