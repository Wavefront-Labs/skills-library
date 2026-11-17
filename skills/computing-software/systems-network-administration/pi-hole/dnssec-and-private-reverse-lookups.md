---
id: computing-software.systems-network-administration.pi-hole.dnssec-and-private-reverse-lookups
name: dnssec-and-private-reverse-lookups
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-dnssec, bogus-priv, dnssec-cache-size]
level: advanced
status: docs-checked
description: "Enable DNSSEC validation in Pi-hole, understand its requirements, and handle private-range reverse lookups."
sources: ["https://docs.pi-hole.net/ftldns/configfile/", "https://docs.pi-hole.net/ftldns/dns-resolver/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNSSEC and private reverse lookups

**DNSSEC.** `dns.dnssec` (default `false`) validates replies using DNSSEC.

- Internally generated DNSSEC queries are analysed and shown unless `dns.showDNSSEC` is `false` (default `true`).
- Cache size is `dns.cache.size` (default `10000` in the configuration reference; the older DNS resolver page still says 150, so trust the reference).

Enable it:

```bash
sudo pihole-FTL --config dns.dnssec true
```

**Private reverse lookups.** `dns.bogusPriv` (default `true`) answers reverse lookups for private ranges such as `192.168.x.y` that are not found in `/etc/hosts` or the DHCP leases with "no such domain" rather than forwarding them upstream. Reverse servers are configured with `dns.revServers`.

**Analysis scope.** `dns.analyzeOnlyAandAAAA` (default `false`) restricts statistics to A and AAAA queries.

**Local interface PTR.** `dns.piholePTR` controls replies for PTR queries about the Pi-hole's own interface addresses: `NONE`, `HOSTNAME`, `HOSTNAMEFQDN` or `PI.HOLE` (default).

**Checklist**

1. Enable `dns.dnssec` with the CLI.
2. Check the query log for DNSSEC-related entries after enabling.
3. Hide them with `dns.showDNSSEC` if they are noise.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile); DNS resolver (ftldns/dns-resolver). Removed the claims that the cache cannot go below 150 entries with DNSSEC, that the upstream must support DNSSEC, and the Unbound advice (none is on the pages). The DNS resolver page says the default cache size is 150 names but the configuration reference says 10000; the skill points to the reference as the current one.
Method: documentation only; no commands were run.
