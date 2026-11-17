---
id: computing-software.systems-network-administration.apache-guacamole.ldap-multi-server
name: ldap-multi-server
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, ldap, ldap-servers-yml, multiple-ldap-servers, match-usernames, active-directory, failover]
level: advanced
status: draft
description: "Use several LDAP or AD servers in Guacamole via ldap-servers.yml: key naming, property defaults, ordered attempts, and match-usernames regex routing."
sources:
  - https://guacamole.apache.org/doc/gug/ldap-auth.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiple LDAP servers (ldap-servers.yml)

Place `ldap-servers.yml` in `GUACAMOLE_HOME`. It is a YAML list; each entry's keys are the LDAP property names without the `ldap-` prefix.

```yaml
- hostname: dc1.example.com
  user-base-dn: ou=people,dc=example,dc=com
  username-attribute: sAMAccountName
  match-usernames: '^(.+)@example\.com$'
- hostname: ldap2.example.net
  user-base-dn: ou=staff,dc=example,dc=net
  username-attribute: uid
```
Rules:
- Values in `guacamole.properties` are defaults for every server; entries override them.
- Servers are tried in order until one authenticates the user.
- `match-usernames`: a Java regex (or list); the capturing group becomes the username. A server only handles logins that match.
- For AD use `sAMAccountName` as the username attribute (the manual's multi-server example does).

Tips:
- Put narrower `match-usernames` servers first to avoid sending every password to every directory.
- Use LDAPS or STARTTLS on each entry via `encryption-method`.

Base properties are in apache-guacamole.ldap-auth-config.

Verify: a user matching the first pattern authenticates against server one, and a non-matching one reaches server two (check Tomcat logs).
