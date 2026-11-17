---
id: computing-software.cryptography-implementation.protocol-implementation.tls13-0-rtt-early-data-and-anti-replay
name: tls13-0-rtt-early-data-and-anti-replay
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-1-3, 0-rtt-replay, early-data, rfc8470, anti-replay]
level: advanced
status: docs-checked
description: "Decide whether to enable TLS 1.3 0-RTT, and if so make it safe: replay windows, single-use tickets, idempotent-only requests, Early-Data header and 425 Too Early."
sources: ["https://www.rfc-editor.org/rfc/rfc8446", "https://www.rfc-editor.org/rfc/rfc8470", "https://blog.cloudflare.com/introducing-0-rtt/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 0-RTT early data and anti-replay

0-RTT lets a resuming client send application data in its first flight, encrypted under a key
derived only from the PSK. That data has **no forward secrecy** and **can be replayed** by an
attacker who captures it. TLS itself cannot fully prevent replay across servers.

## Default: leave it off
Enable only when the latency win is measured and the application can tolerate replays. Check
your server's default and set it explicitly.

## If you enable it
1. **Restrict what may run in early data**: only requests safe to replay (HTTP safe methods with no
   state change, RFC 8470). Never logins, payments, POSTs. RFC 8446 says clients MUST only send early
   data they deem safe to replay, because they cannot know which anti-replay mechanism the server has.
2. **Tell the application**: an intermediary that terminated TLS must add `Early-Data: 1` (RFC 8470) to
   requests that arrived in early data; the origin answers `425 Too Early` for anything it cannot
   process safely, and the client must retry the request after the handshake completes.
3. **Server anti-replay (RFC 8446 section 8)**: every server instance must accept 0-RTT for the same
   handshake at most once. Options:
   - Single-use tickets (section 8.1): keep a database of valid tickets and delete each on use.
   - ClientHello recording (section 8.2): store a unique value from the ClientHello (random or the
     validated PSK binder) within a time window and reject duplicates. Derive the key only from
     validated parts. Reject 0-RTT for a freshly started instance while the window overlaps startup.
   - Freshness check (section 8.3): compute `expected_arrival_time` from `obfuscated_ticket_age`
     minus `ticket_age_add`, and reject 0-RTT if it differs from server time by more than a window;
     the RFC suggests on the order of ten seconds for Internet clients. Freshness alone does not
     stop replays inside the window.
   - Without shared state, a fleet can be replayed once per zone or node; the RFC's best option is one
     authoritative zone per ticket.
4. **Cap size**: `max_early_data_size` in the ticket limits how much early data a server accepts.
5. **Rejecting is always safe**: the server can ignore early data and complete a 1-RTT handshake;
   clients must be ready to resend.

## Implementation checks
- Early data uses `client_early_traffic_secret`; it must not be confused with handshake keys.
- Early data is not permitted after a HelloRetryRequest; the client removes the `early_data` extension.
- The ALPN protocol and cipher suite hash must match the original session or early data is rejected.
- Application-level retry behaviour already needs replay defences that TLS cannot provide.

## Verify
- [ ] `openssl s_client -sess_in s.pem -early_data req.txt` shows early data accepted only on
      endpoints meant to allow it (both options exist in OpenSSL 3.2.3's s_client help).
- [ ] A replayed early-data POST gets 425 or is not executed twice.
- [ ] Anti-replay store or single-use tickets are shared across the nodes that accept 0-RTT.

## Checked
Date: 2026-10-31. Confirmed in RFC 8446 (sections 4.1.2, 8, 8.1 to 8.3, appendix E.5) and RFC 8470: replay
classes, at-most-once per instance, single-use tickets, ClientHello recording, freshness formula and
ten-second window, no early data after HelloRetryRequest, ALPN match, Early-Data header, 425 and client retry.
Ran `openssl s_client -help` (3.2.3): `-early_data`, `-sess_in`, `-sess_out` exist. Removed: nginx and
OpenSSL default-off claims, the 16 KiB example, the client-authentication-inheritance claim (not confirmed).
Method: documentation only; no commands were run beyond the read-only `openssl s_client -help`.
