---
id: computing-software.systems-network-administration.pki-tls-administration.zero-rtt-early-data
name: zero-rtt-early-data
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [zero-rtt-early-data, pki-session, tls13, early-data, 0-rtt, replay, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Decide on TLS 1.3 0-RTT: replay risk, anti-replay mechanisms, and the HTTP Early-Data header and 425 status (RFC 8446 and RFC 8470)."
sources:
  - https://www.rfc-editor.org/rfc/rfc8446
  - https://datatracker.ietf.org/doc/html/rfc8470
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 0-RTT early data
Goal: reduce latency only where replay cannot cause harm.
- 0-RTT (RFC 8446 section 2.3) lets a client send data in its first flight using a PSK from a previous handshake or from out of band. It is weaker than other TLS data: it is not forward secret, and there is no guarantee of non-replay between connections. Data cannot be duplicated within one connection.
- Servers SHOULD provide replay safety using one of the methods in section 8 or an equivalent; since clients cannot know whether servers do, clients MUST only send early data they deem safe to replay.
- Section 8 mechanisms: single-use tickets (8.1), recording ClientHello values (the random or the validated PSK binder) within a time window (8.2), and freshness checks on the ticket age (8.3). Freshness checks alone are not enough to prevent replays; the RFC suggests windows on the order of ten seconds for Internet clients.
- Minimum requirement: every server instance MUST accept 0-RTT for the same handshake at most once, so replays are limited to the number of instances; servers SHOULD limit further when feasible. Freshly started servers SHOULD reject 0-RTT while their recording window overlaps startup time.
- Multi-zone deployments: the best protection is one authoritative storage zone per ticket, refusing 0-RTT elsewhere. Separate per-zone storage limits replays to once per zone, and application-level duplication remains possible.
- HTTP (RFC 8470): the `Early-Data` request header has the single value `1`. An intermediary forwarding a request before its own handshake completes MUST add it, and MUST NOT remove it. It must not appear in responses or in a `Connection` header.
- A request with `Early-Data: 1` that cannot be safely processed MUST be rejected with `425 (Too Early)`; waiting for the handshake does not make it safe. User agents SHOULD retry a 425 automatically, but not in early data. A 425 is not cacheable by default.
- Method safety is one way to judge replay risk, but some resources have side effects with safe methods. RFC 8470 recommends letting resources configure explicitly whether early data is appropriate; absent that, origin servers MUST either reject early data or ensure requests are not processed before the handshake completes.
- Default stance (judgement, not from the RFCs): leave it off unless you have confirmed which resources tolerate replays.
- Server directives (nginx, HAProxy) are not covered by the cited pages; use your server's documentation for the enabling setting and header pass-through.
Verify:
- [ ] A test client sending a request in early data reaches your origin with `Early-Data: 1` set.
- [ ] A replayed request that is unsafe to repeat is answered with 425 and is retried by the client after the handshake.

## Checked
Confirmed 2026-11-08 against RFC 8446 sections 2.3 and 8 (8.1 to 8.3) and RFC 8470 sections 3, 5.1, 5.2, 6. Removed: the nginx and HAProxy directives (including "confirm" items), the `openssl s_client -early_data` check, the CDN/static-content advice, and the "attacker replays an authenticated POST within the ticket window" example (the RFC describes replay generally, not this case).
Method: docs-only read of cited pages, 2026-11-08
