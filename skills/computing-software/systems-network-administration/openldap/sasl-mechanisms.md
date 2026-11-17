---
id: computing-software.systems-network-administration.openldap.sasl-mechanisms
name: sasl-mechanisms
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, sasl, gssapi, digest-md5, external, ldapi, authentication]
level: practitioner
status: docs-checked
description: "Use SASL with OpenLDAP: GSSAPI, DIGEST-MD5, EXTERNAL via TLS or ldapi, PLAIN, and the identity DN each mechanism produces under cn=auth."
sources:
  - https://www.openldap.org/doc/admin26/sasl.html
  - https://www.openldap.org/doc/admin26/slapdconf2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SASL mechanisms
Client selection: `-Y <mech>`, `-U authcid`, `-X authzid`.

- **GSSAPI (Kerberos V)**: create service principal `ldap/directory.example.com@EXAMPLE.COM` in the keytab (normally `/etc/krb5.keytab`); clients use `-Y GSSAPI`. Identity: `uid=<primary[/instance][@realm]>,cn=gssapi,cn=auth`.
- **DIGEST-MD5**: secrets in Cyrus sasldb (`saslpasswd2 -c <user>`) or in the directory as plaintext `userPassword` with `password-hash {CLEARTEXT}`. Identity: `uid=<user>,cn=<realm>,cn=digest-md5,cn=auth`. Example: `ldapsearch -Y DIGEST-MD5 -U u000997 ...`.
- **EXTERNAL over TLS**: identity is the client certificate Subject DN in LDAP order; needs `TLSVerifyClient` set (not `never`).
- **EXTERNAL over ldapi:///**: identity `gidNumber=<n>+uidNumber=<n>,cn=peercred,cn=external,cn=auth`. Typical admin access:
`ldapsearch -Y EXTERNAL -H ldapi:/// -b cn=config`
- **PLAIN/LOGIN**: only over TLS. **CRAM-MD5**: deprecated for DIGEST-MD5. KERBEROS_V4 is deprecated.

`olcSaslRealm` inserts a realm component, so `kurt` becomes `uid=kurt,cn=example.com,cn=gssapi,cn=auth`. Default `olcSaslSecProps` is `noanonymous,noplain` with `minssf` 0 and `maxbufsize` 65536.

Map these identities to directory DNs with `authz-regexp`. Verify with `ldapwhoami -Y <mech>`.

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 Administrator's Guide Using SASL chapter and slapd-config(5): GSSAPI service principal and keytab, the uid=<primary[/instance][@realm]>,cn=gssapi,cn=auth form, olcSaslRealm effect (uid=kurt,cn=example.com,cn=gssapi,cn=auth), DIGEST-MD5 with saslpasswd2 -c or password-hash {CLEARTEXT}, the DIGEST-MD5 example, EXTERNAL via TLS needing TLSVerifyClient, ldapi peercred identity form, PLAIN and LOGIN only with TLS, CRAM-MD5 and KERBEROS_V4 deprecated, authz-regexp mapping, ldapwhoami, olcSaslSecProps defaults. Removed the -R option, which the chapter does not mention.

Method: documentation only; no commands were run.
