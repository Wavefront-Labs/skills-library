---
id: computing-software.email-administration.dovecot.proxy-forwarding-id-xclient-parameters
name: proxy-forwarding-id-xclient-parameters
category: computing-software
field: email-administration
product: dovecot
tags: [proxy-forwarding, xclient, imap-id, x-proxy-ttl, session-id, forward-variables]
level: advanced
status: docs-checked
description: "Which parameters proxies forward over IMAP ID, POP3 and ManageSieve XCLIENT, and SMTP and LMTP XCLIENT, with limits and TTL loop protection."
sources:
  - https://doc.dovecot.org/main/core/config/proxy/forwarding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forwarding requires that the sender be in `login_trusted_networks`. IMAP uses an extended ID command (RFC 2971); POP3 and ManageSieve use XCLIENT with space-separated `field=value` pairs; submission and LMTP use SMTP XCLIENT.

IMAP ID limits: keys up to 30 bytes, values up to 1024 octets (1025 gives "BYE Input buffer full, aborting"), and 30 pairs per the RFC, though Dovecot imposes no pair limit. Keys include `x-originating-ip`, `x-originating-port`, `x-proxy-ttl`, `x-session-ext-id` and `x-forward-<variable_name>` for forwarded settings variables.

The TTL is decremented at each hop to prevent loops; at 0 the connection is dropped. Session IDs are 1 to 64 bytes of printable ASCII without space, double quote or backslash; an invalid value fails the command (changed in 2.4.6).

POP3 and ManageSieve XCLIENT fields: ADDR and PORT (client), DESTADDR and DESTPORT (server, added 2.4.3), SESSION, TTL, DESTNAME (name from TLS SNI), and FORWARD (base64, tab-separated key=value pairs for the auth process). POP3 has a 1024 byte line limit, which shows as "-ERR Input buffer full, aborting".

SMTP and LMTP fields also include HELO, LOGIN, TIMEOUT and PROTO (the forwarded protocol). ADDR needs the `IPV6:` prefix for IPv6, though Dovecot currently forwards without it, which does not follow Postfix XCLIENT syntax. FORWARD (SMTP/submission) is effectively limited to about 1000 bytes. For LMTP, the RCPT TO command gets XRCPTFORWARD (xtext-encoded, about 900 bytes), and LMTP session IDs may be any length since each hop appends `:P<n>`. Invalid SESSION values get `501 5.5.4`.

## Checked

2026-11-03. Confirmed on the proxy forwarding page: login_trusted_networks requirement, IMAP ID versus XCLIENT, the 30-byte key and 1024-octet value limits and the "BYE Input buffer full, aborting" reply at 1025, no Dovecot limit on pair count, x-originating-ip/port, x-proxy-ttl, x-session-ext-id and x-forward-<variable_name>, session ID rules (1 to 64 printable ASCII bytes, changed 2.4.6), the POP3 1024-byte XCLIENT line limit, the FORWARD size notes (about 1000 bytes SMTP/submission, XRCPTFORWARD about 900 bytes LMTP) and 501 5.5.4 for invalid SESSION. Fixed: the IPv6 prefix note belongs to the SMTP/LMTP ADDR field, not POP3/ManageSieve; listed the POP3 field set as the page gives it.

Method: documentation only; no commands were run.
