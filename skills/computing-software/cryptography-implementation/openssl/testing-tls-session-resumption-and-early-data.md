---
id: computing-software.cryptography-implementation.openssl.testing-tls-session-resumption-and-early-data
name: testing-tls-session-resumption-and-early-data
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, s-client, tls-testing, session-resumption-testing, session-tickets, early-data, 0-rtt]
level: advanced
status: docs-checked
description: "Test TLS session resumption and 0-RTT with s_client: -sess_out/-sess_in, -reconnect, reading Reused vs New, sess_id inspection and checking early data acceptance."
sources: ["https://docs.openssl.org/master/man1/openssl-s_client/", "https://docs.openssl.org/master/man1/openssl-s_server/", "https://docs.openssl.org/master/man1/openssl-sess_id/", "https://github.com/openssl/openssl/blob/master/apps/s_client.c", "https://www.rfc-editor.org/rfc/rfc8446#section-4.6.1"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Testing session resumption and early data

Resumption saves a full handshake (and a certificate verify) per reconnect. Broken resumption
shows up as CPU load and latency, not errors, so test it explicitly.

## TLS 1.3 tickets
```
echo | openssl s_client -connect host:443 -servername host -sess_out sess.pem
openssl s_client -connect host:443 -servername host -sess_in sess.pem </dev/null | grep -E "Reused|New,"
```
- First run must show `New, TLSv1.3`; second `Reused, TLSv1.3`.
- TLS 1.3 tickets arrive after the handshake (NewSessionTicket). Use `echo |` (or `-ign_eof`
  with a short read) so s_client stays long enough to receive one; with `</dev/null` it may exit
  first and save nothing.
- `openssl sess_id -in sess.pem -noout -text` prints the saved session in text form.

## Quick multi-connection check
```
openssl s_client -connect host:443 -servername host -tls1_2 -reconnect </dev/null | grep -cE "^Reused"
```
`-reconnect` reconnects to the same server 5 times using the same session ID, as a test that session caching works.
TLS 1.3 tickets arrive after the handshake, so for TLS 1.3 treat 0 `Reused` as inconclusive and use the
`-sess_out`/`-sess_in` loop above.

## Load balancer pitfalls
- Several servers behind one name must share ticket keys (or a session cache); otherwise a
  ticket from server A fails on server B and you see `New` intermittently. Run the loop above
  20 times and count.
- TLS 1.2 session IDs need a cache shared by all servers; stateless tickets need shared ticket keys (see the
  session-caching and tickets skill).

## 0-RTT early data
```
echo -e "GET / HTTP/1.1\r\nHost: host\r\n\r\n" > req.txt
openssl s_client -connect host:443 -servername host -sess_in sess.pem -early_data req.txt
```
Output reports `Early data was accepted` or `rejected`. Accepted early data can be replayed by
an attacker, so only idempotent requests belong there. If your service doesn't need 0-RTT, confirm that
early data is rejected.

## Local server for comparisons
```
openssl s_server -accept 8443 -cert c.pem -key k.pem -early_data -anti_replay
```
`s_server` cannot use `-early_data` together with `-www`, `-WWW`, `-HTTP` or `-rev`, so this runs as the plain echo
server. Replay protection (`-anti_replay`) is on by default: OpenSSL detects a session ticket used more than once when
TLS 1.3 is negotiated and early data is enabled on the server.

## Verify
- [ ] Repeated `-sess_in` connections show `Reused` against every backend.
- [ ] Ticket lifetime matches your policy (see the lifetime limit in RFC 8446).
- [ ] Early data is rejected unless an explicit, idempotent-only policy enables it.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-s_client(1): `-sess_out`, `-sess_in`, `-reconnect` (5 reconnects with the same session ID), `-ign_eof`, `-early_data file` (resumed sessions only, server must accept); openssl-s_server(1): `-early_data` incompatible with `-www`, `-WWW`, `-HTTP` and `-rev`, `-anti_replay` default on and its detection rule; and the printed strings `New,`/`Reused,` and `Early data was accepted`/`rejected` in apps/s_client.c. Removed version-specific observations, the RFC 8470 and 7-day figures and the claims about `Max Early Data` output, which were not checked.

Method: documentation only; no commands were run.
