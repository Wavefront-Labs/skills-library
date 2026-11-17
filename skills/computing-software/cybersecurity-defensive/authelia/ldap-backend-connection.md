---
id: computing-software.cybersecurity-defensive.authelia.ldap-backend-connection
name: ldap-backend-connection
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, ldap, ldaps, starttls, connection-pooling, authentication-backend, directory]
level: practitioner
status: docs-checked
description: "Connect Authelia to an LDAP server with address schemes, StartTLS or LDAPS, timeouts, connection pooling and the service account bind."
sources:
  - https://www.authelia.com/configuration/first-factor/ldap/
  - https://www.authelia.com/integration/ldap/introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The LDAP backend delegates authentication and group lookup to a directory.

```yaml
authentication_backend:
  ldap:
    address: 'ldaps://ldap.example.com'
    implementation: 'custom'
    timeout: '5s'
    start_tls: false
    tls:
      server_name: 'ldap.example.com'
      skip_verify: false
      minimum_version: 'TLS1.2'
    pooling:
      enable: true
      count: 5
      retries: 2
      timeout: '10 seconds'
    base_dn: 'DC=example,DC=com'
    user: 'CN=authelia,OU=service,DC=example,DC=com'
    password: '<LDAP_BIND_PASSWORD>'
```

- `address` is `[<scheme>://]<host>[:<port>]` with scheme `ldap`, `ldaps` or `ldapi`. The default scheme is `ldaps`, or `ldapi` when the value is an absolute path. An `ldapi` URL points to a unix socket the Authelia user can access, such as `ldapi:///var/run/slapd.sock`.
- `start_tls` upgrades a plain connection; it is not commonly used, and the docs say LDAPS is slightly more secure because the initial connection is otherwise plain text.
- `timeout` (default 5 seconds) is the timeout for dialing the connection.
- `pooling` is off by default (`enable: false`; the example above turns it on). When enabled it keeps `count` (default 5) connections available and makes `retries` (default 2) attempts to get a free one within `pooling.timeout`, whose default is 20 seconds (the page's example shows 10 seconds).
- `user` and `password` are required: the service account used for lookups and password changes. This service-user bind is the method Authelia primarily supports; Authelia does not support end-user binding except to check passwords, and end-user binding cannot support password reset. Use a service user with minimal permissions and a random 64+ character password.
- `permit_unauthenticated_bind` is strongly discouraged and requires a blank `password` and `password_reset.disable: true`.
- `permit_referrals` (default false) follows referrals, useful with read-only servers needing write referrals. `base_dn` is prefixed by `additional_users_dn` or `additional_groups_dn`.
- Users must be uniquely identified by a single-valued attribute; duplicates make authentication fail. The page recommends `sAMAccountName` for Active Directory and `uid` elsewhere. Users need an email for password reset and second factor registration.
- `tls` uses the system trust store by default, extendable with `certificates_directory`.

Check: log in with a directory user; if the bind or address is wrong, the login fails with an error in the Authelia log (the pages do not describe a specific success message).

## Checked

2026-11-08. Read in full: first-factor/ldap, integration/ldap/introduction. Corrected pooling defaults (disabled, timeout 20 seconds), unauthenticated bind requirements and removed an unsupported log check.

Method: documentation only; no commands were run.
