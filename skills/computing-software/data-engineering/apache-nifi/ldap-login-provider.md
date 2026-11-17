---
id: computing-software.data-engineering.apache-nifi.ldap-login-provider
name: ldap-login-provider
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, ldap, ldap-provider, login-identity-providers, authentication]
level: practitioner
status: docs-checked
description: "Configure ldap-provider in login-identity-providers.xml: authentication strategy, TLS properties, URL, user search base and filter, identity strategy and expiration."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP login

Set `nifi.security.user.login.identity.provider=ldap-provider` in nifi.properties; define provider `ldap-provider` (class `org.apache.nifi.ldap.LdapProvider`) in `login-identity-providers.xml`.

Properties:
- `Authentication Strategy`: `ANONYMOUS`, `SIMPLE`, `LDAPS` or `START_TLS`.
- `Manager DN`, `Manager Password`.
- `TLS - Keystore/Truststore` (+ Password, Type), `TLS - Client Auth` (`REQUIRED`, `WANT`, `NONE`), `TLS - Protocol`, `TLS - Shutdown Gracefully` (false).
- `Referral Strategy`: `FOLLOW`, `IGNORE` or `THROW` (the sample file uses `FOLLOW`).
- `Connect Timeout` and `Read Timeout`: durations; the guide's example and the sample file use `10 secs`.
- `Url`: space-separated `ldap://host:port` values.
- `User Search Base`, `User Search Filter` (example `sAMAccountName={0}`).
- `Identity Strategy`: `USE_DN` (the default when the property is missing) or `USE_USERNAME`.
- `Authentication Expiration`: how long a login stays valid before the user must log in again; the sample file uses `12 hours` (the guide gives no default for the LDAP provider).

Verify: log in with a directory user; the identity shown matches the chosen Identity Strategy.

## Checked

Confirmed in the NiFi Administration Guide, Lightweight Directory Access Protocol (LDAP): the nifi.properties setting, the sample provider block in login-identity-providers.xml with class org.apache.nifi.ldap.LdapProvider, and every property name, allowed value and example listed above. The earlier wording that implied 12 hours and 10 secs were defaults was corrected to sample or example values.

Method: docs-only read of cited pages, 2026-11-08
