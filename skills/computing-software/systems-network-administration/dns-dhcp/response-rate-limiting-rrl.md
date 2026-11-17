---
id: computing-software.systems-network-administration.dns-dhcp.response-rate-limiting-rrl
name: response-rate-limiting-rrl
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, dns-security, rrl, response-rate-limiting, rate-limit, amplification, reflection-attack, slip, tc-bit, log-only, authoritative-dns, ddos]
level: practitioner
status: verified
description: "Stop authoritative BIND servers being used for reflection attacks with Response Rate Limiting: options, slip and truncation, log-only trials, exemptions."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html#response-rate-limiting
  - https://kb.isc.org/docs/aa-00994
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Response Rate Limiting (RRL)

Attackers send small queries with a spoofed source (the victim) to authoritative servers, which
reply with large answers to the victim. RRL limits identical responses to the same client
netblock, so your servers stop being an effective amplifier.

## Configure (authoritative servers)
```
options {
    rate-limit {
        responses-per-second 10;     // identical responses per client /24 (or /56 for IPv6); default 0 = no limit
        nxdomains-per-second 10;
        errors-per-second 5;
        window 15;                   // seconds of history (default 15, range 1-3600)
        slip 2;                      // default; every 2nd limited response is a small reply (TC=1, or BADCOOKIE if a client cookie was sent)
        ipv4-prefix-length 24;       // defaults 24 and 56
        ipv6-prefix-length 56;
        exempt-clients { 10.0.0.0/8; 192.0.2.53; };   // monitoring, your own resolvers
        // log-only yes;             // start here
    };
};
```
**Slip** matters (ARM, 0 to 10): without a cookie, a slipped reply is truncated (TC=1) so a legitimate client retries over
TCP (exempt from limiting); with a client cookie it is a BADCOOKIE carrying a server cookie the client can reuse. REFUSED
and SERVFAIL cannot be truncated and leak at the slip rate. `slip 0` drops everything over the limit (harsher), `slip 1`
slips every response.

## Rollout
1. `log-only yes;` for a week. The `rate-limit` log category carries start, periodic and final notices of a limited
   stream (about a minute after limiting stops); limiting of individual requests is logged in `query-errors`:
   ```
   logging { channel rl { file "/var/log/named/ratelimit.log" versions 3 size 20m; print-time yes; };
             category rate-limit { rl; }; category query-errors { rl; }; };
   ```
2. Check which clients would be limited: large shared resolvers aggregate many users behind few IPs, so watch
   how often identical answers exceed the rate for them.
3. Remove `log-only`; monitor `rndc stats` counters (`RateDropped`, `RateSlipped`; truncated ones also count in
   `RespTruncated`).

## Recursive resolvers
RRL is designed for authoritative servers. On resolvers, prevent abuse by not being open
(allow-recursion) and use `fetches-per-server` / `fetches-per-zone` (maximum simultaneous iterative queries to one
server or zone) to limit upstream floods such as random-subdomain attacks.

## Verify
- [ ] `dnsperf` or a scripted burst of identical queries from one test host shows drops/slips in the log.
- [ ] Normal resolution unaffected (monitoring probes exempt and green).
