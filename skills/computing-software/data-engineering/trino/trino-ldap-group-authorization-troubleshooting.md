---
id: computing-software.data-engineering.trino.trino-ldap-group-authorization-troubleshooting
name: trino-ldap-group-authorization-troubleshooting
category: computing-software
field: data-engineering
product: trino
tags: [ldap-group-auth-pattern, ldap-bind-dn, ldap-service-user, ldap-troubleshooting, subject-alternative-name]
level: advanced
status: docs-checked
description: "Restrict Trino LDAP logins by group membership, use an LDAP service user, and fix common LDAP and CLI TLS errors such as missing SAN."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/ldap.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino ldap group authorization troubleshooting

Group-restricted login: add `ldap.user-base-dn` (for example `OU=America,DC=corp,DC=example,DC=com`) and `ldap.group-auth-pattern`, an LDAP query containing `${USER}` that must succeed for the user to be authorised.

Active Directory example:

```text
ldap.group-auth-pattern=(&(objectClass=person)(sAMAccountName=${USER})(memberof=CN=AuthorizedGroup,OU=Asia,DC=corp,DC=example,DC=com))
```

OpenLDAP uses `uid=${USER}` and an `inetOrgPerson` class; the `memberOf` overlay must be enabled. For membership in any of several groups use an OR: `(&(|(memberOf=CN=normal_group,DC=corp,DC=com)(memberOf=CN=another_group,DC=com))(objectClass=inetOrgPerson)(uid=${USER}))`.

Service user mode: define `ldap.bind-dn` (such as `CN=admin,OU=CITY_OU,OU=STATE_OU,DC=domain`), `ldap.bind-password` and `ldap.group-auth-pattern`. Trino first runs the group query with the service account, extracts the user's DN from the result, then validates the password by opening an LDAP context with that DN.

CLI invocation uses `--server https://...`, `--keystore-path`, `--keystore-password`, `--truststore-path`, `--truststore-password`, `--user` and `--password`.

Troubleshooting:
- Set log level `io.trino.plugin.password=DEBUG` to debug Trino-to-LDAP issues.
- For CLI TLS problems run the executable JAR with `java -Djavax.net.debug=ssl`.
- `No subject alternative names present`: the coordinator certificate lacks a SAN for the IP used in `--server`; reissue it with the right SAN.
- After JDK 8u181, LDAPS endpoint identification is on by default and can fail with `No subject alternative DNS name matching ldapserver found`. Fix the LDAP server certificate; as a temporary measure add `-Dcom.sun.jndi.ldap.object.disableEndpointIdentification=true` to `jvm.config`.

## Checked

2026-11-04. Read against the Trino docs page `security/ldap.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
