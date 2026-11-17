---
id: computing-software.cybersecurity-defensive.dex.dex-ldap-connector-overview-and-security
name: dex-ldap-connector-overview-and-security
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [ldap, connector, security, starttls]
level: practitioner
status: docs-checked
description: "Understand the Dex LDAP connector: two queries (user then groups), plaintext password binds, and TLS options host, startTLS and rootCA."
sources:
  - https://dexidp.io/docs/connectors/ldap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The LDAP connector gives email/password login backed by a directory. It runs two primary queries: find the user from the credentials, then search for groups using the user entry. It first binds with `bindDN` and `bindPW`, searches for the username, then binds as the found user to verify the password. A search returning multiple entries is ambiguous and returns an error.

Security: Dex binds to the LDAP server with the end user's plain text password. Some LDAP servers accept hashed passwords but Dex does not support hashing, so protect the transport. Insecure connections are currently allowed while the project verifies compatibility, and that option may be removed.

Connection options:

```yaml
connectors:
- type: ldap
  id: ldap
  name: LDAP
  config:
    host: ldap.example.com:636
    # insecureNoSSL: true
    # startTLS: true
    rootCA: /etc/dex/ldap.ca
```

- Port defaults to 389 for insecure or StartTLS connections and 636 otherwise.
- `startTLS: true` connects with `ldap://` then issues StartTLS. Unset, `ldaps://` is used.
- `rootCA` is a trusted root file; `rootCAData` takes base64 PEM inline.
- `insecureSkipVerify` turns off certificate checks and is for exploration only.

Try it: the repo's `examples/ldap` runs OpenLDAP via docker-compose; log in as `janedoe@example.com` / `foo`.

## Checked

2026-11-03: read against Dex docs, LDAP connector (https://dexidp.io/docs/connectors/ldap/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
