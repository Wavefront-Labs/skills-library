---
id: computing-software.systems-network-administration.dns-dhcp.pi-hole-filtering-resolver
name: pi-hole-filtering-resolver
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, pihole, dns-filtering, ad-blocking, unbound, dhcp]
level: practitioner
status: docs-checked
description: "Run Pi-hole as a filtering DNS resolver and point it at a local Unbound recursive resolver instead of a third-party upstream."
sources:
  - https://docs.pi-hole.net/guides/dns/unbound/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pi-hole filtering resolver

Pi-hole includes a caching and forwarding DNS server, FTLDNS. For a client query it checks its cache, then the blocking lists, and otherwise forwards the query to the configured upstream DNS servers, caching the answer.

## Why add a local recursive resolver
- A forwarding Pi-hole raises the question of whom to trust: the upstream provider sees your queries, and a poisoned large upstream affects many users. Running your own small recursive server reduces that exposure.
- With a local recursive resolver, a cache miss is resolved by walking root, TLD and authoritative servers directly, so no single upstream sees the full path of your lookups.
- Drawback: the first lookup, especially under an unseen TLD or with DNSSEC, can take up to a second or more; later lookups under the same TLD are usually under 0.1 s. Both Pi-hole and the recursive server cache.

## Check the network first
Some ISPs, parental-filter software and consumer router firmware intercept outbound port 53 and silently redirect it, which stops Unbound reaching the root servers. The guide tests against a.root-servers.net (198.41.0.4) from the machine that will run Unbound:
1. UDP: query for the root NS records with recursion off. A real root server answers with the `aa` flag and without `ra`; an interceptor shows `ra` and usually no `aa`.
2. TCP: repeat the query over TCP. Unbound relies on TCP/53 for large DNSSEC responses and retries, and some CG-NAT setups pass UDP but drop TCP DNS.
3. CHAOS: query `version.bind` in class CH, type TXT. A real root server returns `ATLAS`; interception proxies often return something else, time out or return SERVFAIL.
If any test fails, investigate before installing Unbound.

## Set up Unbound for Pi-hole (Debian or Ubuntu)
- Install the distribution `unbound` package; it brings the root hints file via `dns-root-data` and keeps it updated. Set the `root-hints:` option only if you downloaded the file yourself.
- Put a config in `/etc/unbound/unbound.conf.d/pi-hole.conf` (on some Red Hat family systems up to CentOS 10, `/etc/unbound/conf.d/pi-hole.conf`). The guide's highlights: listen only on 127.0.0.1 port 5335, UDP and TCP, verify DNSSEC signatures and discard BOGUS domains, plus hardening options such as `harden-glue`, `harden-dnssec-stripped`, `use-caps-for-id: no`, `edns-buffer-size: 1232`, `prefetch: yes` and `private-address` ranges.
- Restart Unbound and test with a query to 127.0.0.1 port 5335. Test DNSSEC with `fail01.dnssec.works` (expect SERVFAIL) and `dnssec.works` (expect NOERROR plus the `ad` flag).
- In Pi-hole, set `127.0.0.1#5335` under Settings, DNS, Custom DNS servers and untick all other upstreams, then Save and Apply.
- On Debian Bullseye and later, the `unbound-resolvconf` service can write `nameserver 127.0.0.1` without the port into `/etc/resolv.conf`; the guide has you disable that service and the generated `resolvconf_resolvers.conf` file, then restart Unbound.
- For debugging, raise `verbosity` (0 is errors only, 1 operational information, up to 5) and set a log file; this needs the log file created, owned by `unbound` and an AppArmor exception. High verbosity is not for daily use because Unbound logs a lot.

## Verify
- [ ] A query to Unbound on port 5335 resolves, DNSSEC test names behave as above, and Pi-hole queries show Unbound as the upstream.

## Checked

Confirmed against the Pi-hole documentation guide "unbound" (read in full to the logging section). Removed as not on the cited pages: install one-liner, `pihole` CLI commands, Docker image, group and allowlist management, upstream-choice advice about Quad9 and Cloudflare, conditional forwarding, DHCP role, redundancy and sync tools, IPv6 RDNSS advice, DoH canary domain and port-blocking advice, and the Pi-hole documentation landing page as a source.

Method: docs-checked 2026-11-09 against https://docs.pi-hole.net/guides/dns/unbound/.
