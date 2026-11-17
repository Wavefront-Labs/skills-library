---
id: computing-software.systems-network-administration.dns-dhcp.ddclient-dynamic-home-addresses
name: ddclient-dynamic-home-addresses
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, ddclient, dynamic-dns, ddns-providers]
level: practitioner
status: docs-checked
description: "Keep a DNS name pointed at a changing home or branch IP with ddclient: providers, IP detection, secrets in environment variables."
sources:
  - https://ddclient.net/
  - https://github.com/ddclient/ddclient
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ddclient for dynamic home addresses

ddclient is a Perl client that updates dynamic DNS entries at many providers. It uses `curl` for network access. Its configuration has three parts: general settings, where to find your IP (the "router" setting, for example ipify or a broadband router status page), and the protocol or provider to update.

## Config
The default file is `/etc/ddclient/ddclient.conf` (ddclient 4.x; 3.x used `/etc/ddclient.conf`). Example from the project site:
```
# General config
daemon=300
# Router
usev4=webv4,webv4=ipify-ipv4
# Protocol
protocol=dyndns2
login=myUsername
password=myPassword
myhost.dyndns.org
```
Run as a daemon, this checks every 300 seconds, gets the IPv4 address from ipify, and updates the host at the provider when it changes.

- Supported providers include Cloudflare, DigitalOcean, Hetzner, Gandi, GoDaddy, Porkbun, Namecheap, No-IP and many more. Your own DNS server (ISC BIND, Knot, PowerDNS, Technitium) can be updated with `protocol=nsupdate` (RFC 2136).
- Use the `usev4` and `usev6` parameters rather than the older `use`; version 3.10.0 had a bug that spammed updates to Cloudflare, Hetzner, DigitalOcean and Infomaniak with `use` (fixed in 3.11.2).
- Keep secrets out of the file: appending `_env` to a parameter (version 3.11.0_1 and later) makes ddclient read its value from the named environment variable, for example `password_env=DDCLIENT_PASSWORD`.
- Command-line arguments beat `ddclient.conf`, which beats built-in defaults. Restrict the file with `chmod 600`.
- Some routers need `fw-login` and `fw-password`, and `fwv4=<router address>` reads the WAN IP from a router status page.
- In daemon mode no cron job is needed; if you run from cron instead, force an update periodically so the DNS entry does not go stale.

## Run and test
```
ddclient --daemon=0 --debug --verbose
systemctl enable ddclient.service
```
The first runs once with debug output. If ddclient starts but only sleeps, check that the config section in the verbose output is not empty, which means the config file was not found (common after upgrading from 3.x).

## Gotchas
- In 3.9.1 to 3.11.2 the `ssl` parameter forced HTTPS even for HTTP-only IP-lookup sites; 4.0.0 respects `http://` in a URL.
- Verify the result with a normal DNS lookup of the host name after an address change.

## Verify
- [ ] After the WAN address changes, the record at the provider follows within the daemon interval.

## Checked
Method: docs-checked 2026-11-09 against the ddclient.net project page and the ddclient GitHub README (provider list, requirements, upgrade notes, known issues, troubleshooting), both read in full. Dropped the Cloudflare token example, cache file path, TTL advice, CGNAT note and the Cloudflare API source (a landing page).
