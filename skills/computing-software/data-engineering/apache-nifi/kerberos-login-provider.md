---
id: computing-software.data-engineering.apache-nifi.kerberos-login-provider
name: kerberos-login-provider
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, kerberos, kerberos-provider, spnego, authentication]
level: practitioner
status: docs-checked
description: "Kerberos login in NiFi: kerberos-provider settings, default realm, 12 hour expiry, and the nifi.kerberos.* properties for service principal and SPNEGO single sign-on."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kerberos authentication

Login provider: set `nifi.security.user.login.identity.provider=kerberos-provider`; class `org.apache.nifi.kerberos.KerberosProvider` in `login-identity-providers.xml`.
- `Default Realm` (sample `NIFI.APACHE.ORG`) completes incomplete principals.
- `Authentication Expiration`: how long a login stays valid; the sample file uses 12 hours and the property table gives no default.

Service and SPNEGO keys in nifi.properties (blank by default):
- `nifi.kerberos.krb5.file`
- `nifi.kerberos.service.principal`, `nifi.kerberos.service.keytab.location` (NiFi as a client to other systems)
- `nifi.kerberos.spnego.principal`, `nifi.kerberos.spnego.keytab.location` (authenticating users from client tickets)
- `nifi.kerberos.spengo.authentication.expiration`: 12 hours. The key is misspelled "spengo" in the docs; use it exactly.

Verify: a ticketed browser reaches the UI without a prompt, or a password login with a bare username resolves to the default realm.

## Checked

Checked against the NiFi Administration Guide, Kerberos login provider and Kerberos Properties sections: provider class, the two provider properties, the `nifi.kerberos.*` keys (blank by default), the single krb5 file limit and the 12 hour SPNEGO expiration default (key spelled `spengo`) match. The provider's own expiration was reworded because only the sample shows 12 hours.

Method: docs-only read of cited pages, 2026-11-08
