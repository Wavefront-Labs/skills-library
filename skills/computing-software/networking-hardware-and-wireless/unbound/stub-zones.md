---
id: computing-software.networking-hardware-and-wireless.unbound.stub-zones
name: stub-zones
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, stub-zone, stub-addr, stub-prime, stub-first, internal-zone]
level: practitioner
status: docs-checked
description: "Point a zone at specific authoritative servers with stub-zone: stub-addr versus stub-host, priming, fallback, TLS and cache bypass."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# stub zones
A `stub-zone:` clause (repeatable) makes Unbound query given authoritative nameservers for a zone, rather than finding them through delegation.

- `name:` is the zone.
- `stub-addr:` is a nameserver IP (v4 or v6); `@port` and `#auth-name` are accepted. Preferred.
- `stub-host:` is a nameserver hostname that is resolved first; the manual warns this can create a circular dependency, so `stub-addr` is preferred.
- `stub-prime: yes` (default no) primes the NS set, like root hints: it starts using the zone's currently published nameservers, so an outdated list self-corrects.
- `stub-first: yes` (default no) retries the query without this stub when it would otherwise SERVFAIL, which can fall to a less specific zone or normal recursion. It also works around a `stub-host` circular dependency, but lets queries escape the zone.
- `stub-tls-upstream: yes` (alias `stub-ssl-upstream`, default no) uses TLS; `#auth-name` checks the certificate name, and `#` alone uses `tls-port`.
- `stub-tcp-upstream: yes` (default no) uses TCP only, regardless of the global `tcp-upstream`.
- `stub-no-cache: yes` (default no) does not cache data from the stub; useful to see changes immediately.

Runtime: `unbound-control stub_add [+ipt] zone addr...` (`+i` also adds domain-insecure, `+p` sets prime, otherwise notprime; `+t` uses TLS), `stub_remove [+i] zone`, and `list_stubs` (which includes root hints).

For a stub or forward zone to an unsigned internal zone, `domain-insecure` is the DNSSEC counterpart.

## Checked

2026-11-08. Read the whole Stub Zone Options section of unbound.conf and the stub_add and stub_remove commands. Added stub-tcp-upstream, clarified stub-prime and stub-first semantics and the notprime default of stub_add.

Method: documentation only; no commands were run.
