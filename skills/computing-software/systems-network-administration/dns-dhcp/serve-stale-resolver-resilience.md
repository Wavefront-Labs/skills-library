---
id: computing-software.systems-network-administration.dns-dhcp.serve-stale-resolver-resilience
name: serve-stale-resolver-resilience
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, serve-stale, rfc8767, resolver-resilience, bind, unbound]
level: practitioner
status: docs-checked
description: "Configure serve-stale (RFC 8767) on BIND and Unbound so resolvers answer from expired cache when authoritative servers are unreachable, with safe limits."
sources:
  - https://www.rfc-editor.org/rfc/rfc8767
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-stale-answer-enable
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serve-stale

When a domain's authoritative servers are down (DDoS, provider outage), a resolver can keep answering
with expired cached data instead of SERVFAIL. RFC 8767 defines how.

## BIND
```
options {
    stale-answer-enable yes;
    stale-cache-enable yes;           // keep expired records (default no)
    max-stale-ttl 86400;              // how long past expiry to keep (default 1 day)
    stale-answer-ttl 30;              // TTL given to stale answers (default 30 s)
    stale-answer-client-timeout off;  // off by default; the only supported non-off value is 0
    stale-refresh-time 30;            // after a failure, serve stale without retrying for this long (default 30 s)
};
```
Runtime: `rndc serve-stale on|off` override the configured setting and `rndc serve-stale reset` restores it. Stale answers are logged in the `serve-stale` category.

## Unbound
```
server:
    serve-expired: yes
    serve-expired-ttl: 86400
    serve-expired-client-timeout: 1800   # default; ms to try resolving before answering stale
    serve-expired-reply-ttl: 30
```
`serve-expired-client-timeout: 0` answers stale immediately and refreshes in the background (fast
but can serve stale data after legitimate changes).

## Trade-offs
- Benefit: users keep reaching services during upstream outages.
- Risk: changes during an outage (failover records) are not seen until refresh succeeds.
- Memory: expired records stay cached up to `max-stale-ttl`.

## Test
1. Query a test record, wait until TTL expires.
2. Block egress from the resolver to its authoritative servers.
3. Query again: answer returns with the stale TTL (30 by default; BIND logs the `serve-stale` category).

## Verify
- [ ] With authoritative servers blocked, cached names still resolve with the stale TTL and logs show stale answers.

## Checked
2026-11-01. Confirmed against the BIND 9 ARM (stale-answer-enable, stale-cache-enable default no, max-stale-ttl default 1 day, stale-answer-ttl default 30 s, stale-refresh-time 30 s, stale-answer-client-timeout off or 0 only, rndc serve-stale on/off/reset, serve-stale log category) and the Unbound unbound.conf manual (serve-expired, serve-expired-ttl default 86400, serve-expired-client-timeout default 1800 and 0 behaviour, serve-expired-reply-ttl 30 per RFC 8767). Removed: BIND version gates, rndc status subcommand, the 1800 BIND timeout value (BIND supports only 0), the firewall command and the outage anecdote.
Method: documentation only; no commands were run.
