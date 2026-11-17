---
id: computing-software.data-engineering.trino.trino-ldap-authentication
name: trino-ldap-authentication
category: computing-software
field: data-engineering
product: trino
tags: [ldap, ldap-authentication, user-bind-pattern, active-directory, openldap]
level: advanced
status: docs-checked
description: "Configure Trino LDAP password authentication on the coordinator, including ldap.url, bind patterns for Active Directory and OpenLDAP, TLS stores and timeouts."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/ldap.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino ldap authentication

Trino supports simple LDAP bind authentication only: the client sends username and password over HTTPS and the coordinator validates them against the LDAP service. TLS and the internal shared secret are required.

Coordinator `config.properties` (details in HTTP server properties):

```text
http-server.authentication.type=PASSWORD
http-server.https.enabled=true
http-server.https.port=8443
http-server.https.keystore.path=/etc/trino/keystore.jks
http-server.https.keystore.key=keystore_password
```

Optional `http-server.authentication.password.user-mapping.pattern` (first regex group replaces the user, no match denies; default `(.*)`) or `.user-mapping.file`.

`etc/password-authenticator.properties`:

```text
password-authenticator.name=ldap
ldap.url=ldaps://ldap-server:636
ldap.ssl.truststore.path=/path/to/ldap_server.pem
ldap.user-bind-pattern=${USER}@corp.example.com
```

Properties: `ldap.url` must be `ldap://` or `ldaps://`; plain `ldap://` needs `ldap.allow-insecure=true`. Keystore and truststore paths take PEM or JKS with matching password properties. `ldap.user-bind-pattern` must contain `${USER}` and may list several patterns separated by colons, tried in order until one succeeds. `ldap.ignore-referrals` default `false`; `ldap.cache-ttl` `1h`; `ldap.timeout.connect` and `ldap.timeout.read` `1m`.

Bind pattern by server type: Active Directory `${USER}@<domain>`, such as `${USER}@corp.example.com`; OpenLDAP `uid=${USER},<user DN>`, such as `uid=${USER},OU=America,DC=corp,DC=example,DC=com`.

## Checked

2026-11-04. Read against the Trino docs page `security/ldap.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
