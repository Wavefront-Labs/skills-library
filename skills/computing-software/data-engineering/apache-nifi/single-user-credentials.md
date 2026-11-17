---
id: computing-software.data-engineering.apache-nifi.single-user-credentials
name: single-user-credentials
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, single-user-provider, credentials, login, bcrypt]
level: intro
status: docs-checked
description: "Find the generated NiFi login in nifi-app.log, understand single-user-provider, and change the username and password with nifi.sh set-single-user-credentials."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/getting-started.html
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-user login

Default `nifi.security.user.login.identity.provider` is `single-user-provider`, class `org.apache.nifi.authentication.single.user.SingleUserLoginIdentityProvider`, configured in `login-identity-providers.xml` (`Username` and `Password` are blank in the shipped file).

On first start NiFi generates a 36-character UUID username and a 32-character password, stored with bcrypt. Find them by searching `logs/nifi-app.log` for "Generated Username" and "Generated Password".

Change them:
`./bin/nifi.sh set-single-user-credentials <username> <password>`

Related defaults: `nifi.login.identity.provider.configuration.file` is `./conf/login-identity-providers.xml`.

Verify: log in at the HTTPS UI (default `https://localhost:8443/nifi`) with the generated or newly set pair.

## Checked

Checked against the NiFi Getting Started and Administration Guide User Authentication sections: the default provider and its class, blank Username and Password in the shipped file, the 36-character UUID username, 32-character bcrypt-stored password, the log lines and path, the `set-single-user-credentials` command, the default configuration file path and the 8443 UI port match. Replaced the unsourced restart and rejection claim.

Method: docs-only read of cited pages, 2026-11-08
