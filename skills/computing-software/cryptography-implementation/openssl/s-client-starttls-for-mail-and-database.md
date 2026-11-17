---
id: computing-software.cryptography-implementation.openssl.s-client-starttls-for-mail-and-database
name: s-client-starttls-for-mail-and-database
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, s-client, tls-testing, starttls, smtp-tls, imap-tls, postgres-tls, ldap-tls]
level: practitioner
status: docs-checked
description: "Test STARTTLS and implicit-TLS services with openssl s_client: SMTP, IMAP, POP3, LDAP, PostgreSQL and MySQL, ports, -name, and spotting stripped STARTTLS."
sources: ["https://docs.openssl.org/master/man1/openssl-s_client/", "https://github.com/openssl/openssl/blob/master/apps/s_client.c", "https://www.postgresql.org/docs/current/protocol-flow.html", "https://www.rfc-editor.org/rfc/rfc6698"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STARTTLS testing for mail and database protocols

Many services begin in plaintext and upgrade with a protocol-specific command. s_client speaks
the preamble for you with `-starttls <proto>`.

## Commands by protocol
| Service | `-starttls` keyword | Notes |
|---|---|---|
| SMTP / LMTP | `smtp` / `lmtp` | `-name` sets the EHLO / LHLO name |
| IMAP | `imap` | |
| POP3 | `pop3` | |
| LDAP | `ldap` | |
| PostgreSQL | `postgres` | s_client sends an SSLRequest and continues only if the server answers `S`; for a direct-TLS listener (see the PostgreSQL protocol docs) connect without `-starttls` and use `-alpn postgresql` |
| MySQL | `mysql` | |
| XMPP | `xmpp` / `xmpp-server` | `-xmpphost` or `-name` sets the host |
| FTP | `ftp` | |
| NNTP, Sieve, IRC | `nntp`, `sieve`, `irc` | |
The supported keywords are exactly: smtp, pop3, imap, ftp, xmpp, xmpp-server, irc, postgres, mysql, lmtp, nntp, sieve
and ldap. Use `-connect host:port` with the port your service listens on; a service on an implicit-TLS port is tested
without `-starttls`. Always add `-servername <host>` and `-verify_return_error` as for HTTPS.

```
openssl s_client -connect mx1.example.com:<port> -starttls smtp -name probe.example.net \
  -servername mx1.example.com -verify_return_error -brief </dev/null
```
`-name` sets the EHLO hostname; if it is not given, s_client uses `mail.example.com`.

## What to check
- Certificate matches the hostname clients will verify (the MX hostname for server-to-server mail).
- Protocol and cipher meet policy.
- Check both the STARTTLS and implicit-TLS listeners if both are open.

## Detecting STARTTLS problems
- `Didn't find STARTTLS in server response` = the server did not advertise it, or something in the path removed it;
  compare results from inside and outside the network.
- For PostgreSQL s_client stops unless the server answers the SSLRequest with `S`.
- Clients that silently continue in plaintext when STARTTLS fails are the bug; configure them to require verified TLS
  (see each product's documentation for the setting).

## DANE check
```
openssl s_client -connect mx1.example.com:<port> -starttls smtp \
  -dane_tlsa_domain mx1.example.com -dane_tlsa_rrdata "3 1 1 <hex>" </dev/null
```
`-dane_tlsa_domain` enables RFC 6698 / RFC 7671 DANE authentication with at least one `-dane_tlsa_rrdata` record (usage,
selector, matching type, hex data). On success the output reports `matched EE certificate` at depth 0, `matched TA
certificate` at a positive depth, or `TA public key verified`; `Verified peername` shows the name that matched.

## Verify
- [ ] Every mail/database listener negotiates TLS 1.2+ with a valid, matching certificate.
- [ ] Clients are configured to fail when STARTTLS is unavailable.
- [ ] TLSA records (if published) match the served key; rotate them before rotating keys.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-s_client(1): the exact list of `-starttls` keywords, `-xmpphost`, `-name` (EHLO/LHLO name, default `mail.example.com`), `-dane_tlsa_domain` and `-dane_tlsa_rrdata` semantics and result wording; the `Didn't find STARTTLS in server response` message and the PostgreSQL SSLRequest handling (continues only on `S`) in apps/s_client.c; and in the PostgreSQL protocol documentation that direct TLS requires ALPN with the protocol name `postgresql`. Removed standard port numbers, RFC 8314 and firewall claims, third-party commands (dig, curl, nc) and client configuration option names that were not checked.

Method: documentation only; no commands were run.
