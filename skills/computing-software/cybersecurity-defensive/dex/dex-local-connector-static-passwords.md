---
id: computing-software.cybersecurity-defensive.dex.dex-local-connector-static-passwords
name: dex-local-connector-static-passwords
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [local-connector, static-passwords, bcrypt, enablepassworddb]
level: practitioner
status: docs-checked
description: "Enable the built-in local connector with enablePasswordDB and define users with staticPasswords: email, bcrypt hash, username, userID."
sources:
  - https://dexidp.io/docs/connectors/local/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The built-in local connector is a virtual identity provider that stores login credentials in Dex's storage. Enable it with:

```yaml
enablePasswordDB: true
```

Users can be added statically in the config or dynamically through the gRPC API (adds, updates and removals).

Static users use `staticPasswords`:

```yaml
staticPasswords:
  - email: "admin@example.com"
    hash: "$2a$10$2b2cU8CPhOTaGrs1HRQuAueS7JTT5ZHsHSzYiFPm1leZck7Mc8T4W"
    username: "admin"
    userID: "08a8684b-db88-4b73-90a9-3cd1661f5466"
```

Fields:

- `email`: the main identifier of the user.
- `hash`: bcrypt hash of the password.
- `username`: username for the user.
- `userID`: unique id.

Generate a hash for the string `password` with:

```bash
echo password | htpasswd -BinC 10 admin | cut -d: -f2
```

Gotchas:

- Never store a plain text password in `hash`; it must be a bcrypt hash.
- `userID` is the unique id of the user, so give each user a distinct value.
- To log in with a password via API (grant type `password`) you also need `oauth2.passwordConnector: local`.

## Checked

2026-11-03: read against Dex docs, local connector (https://dexidp.io/docs/connectors/local/); Dex docs, OAuth2 configuration (https://dexidp.io/docs/configuration/oauth2/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
