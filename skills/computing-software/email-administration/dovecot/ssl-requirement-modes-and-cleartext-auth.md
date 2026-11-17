---
id: computing-software.email-administration.dovecot.ssl-requirement-modes-and-cleartext-auth
name: ssl-requirement-modes-and-cleartext-auth
category: computing-software
field: email-administration
product: dovecot
tags: [ssl-required, auth-allow-cleartext, logindisabled, tls-modes, ssl-server-cert-file, ssl-server-key-file]
level: practitioner
status: docs-checked
description: "Decide between ssl no, yes and required, and how auth_allow_cleartext changes whether passwords can cross an unencrypted connection."
sources:
  - https://doc.dovecot.org/main/core/config/ssl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core settings are the certificate (`ssl_server_cert_file`) and key (`ssl_server_key_file`), which can live in one file. The certificate may be world-readable; the key should be readable only by root (or an ssl-certs group). Dovecot opens both while still root, so give the dovecot user no access to the key. Set `ssl = yes` globally if any protocol needs TLS, or Dovecot will not listen on SSL ports; that also demands a global certificate and key even if you override them per protocol.

Modes:
- `ssl = no`: TLS disabled.
- `ssl = yes` with `auth_allow_cleartext = yes`: TLS offered, not required; cleartext login allowed without it. Insecure.
- `ssl = yes` with `auth_allow_cleartext = no`: TLS offered; cleartext mechanisms need TLS first, but non-cleartext mechanisms may still run without it.
- `ssl = required`: TLS always required, any authentication attempt before TLS fails. This is unrelated to STARTTLS; both implicit TLS and STARTTLS satisfy it.

With only cleartext mechanisms enabled (such as plain and login) and `auth_allow_cleartext = no`, `yes` and `required` behave the same. The difference is that `required` protects the whole connection, while `auth_allow_cleartext = no` only protects authentication.

Even with `yes` or `required`, a client may send a password before enabling TLS. Dovecot advertises IMAP `LOGINDISABLED`, but many clients ignore it and cannot be stopped; POP3 has no equivalent capability.

## Checked
2026-11-09. Read the Dovecot core/config/ssl page (TLS requirement section). Confirmed each statement above: file
permissions, root opening the files, global `ssl = yes`, the mode behaviours, `required` versus STARTTLS, the equivalence
case, and the LOGINDISABLED and POP3 notes. Nothing removed.
Method: documentation only; no commands were run.
