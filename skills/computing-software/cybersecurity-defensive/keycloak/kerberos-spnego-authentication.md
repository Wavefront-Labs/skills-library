---
id: computing-software.cybersecurity-defensive.keycloak.kerberos-spnego-authentication
name: kerberos-spnego-authentication
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, kerberos, spnego, keytab, negotiate]
level: practitioner
status: docs-checked
description: "Enable Kerberos SPNEGO single sign-on in Keycloak with an HTTP service principal, keytab and the Kerberos user federation provider."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/authentication/kerberos.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kerberos spnego authentication
Keycloak supports login with a Kerberos ticket through SPNEGO; the browser authenticates transparently after the desktop login, and Keycloak falls back to the normal login screen when no ticket is available. Setup has three parts: the Kerberos server (KDC), the Keycloak server, and the client machines.

1. Kerberos server: add user principals and a service principal for the `HTTP` service. For a server at `www.mydomain.org`, MIT Kerberos example:
```
sudo kadmin.local
addprinc -randkey HTTP/www.mydomain.org@MYDOMAIN.ORG
ktadd -k /tmp/http.keytab HTTP/www.mydomain.org@MYDOMAIN.ORG
```
2. Keycloak server host: configure the Kerberos client (`/etc/krb5.conf` on Linux) with your realm and a `domain_realm` section (`.mydomain.org = MYDOMAIN.ORG` and `mydomain.org = MYDOMAIN.ORG`). Make the keytab accessible to the process running Keycloak; for production, readable by that process only.
3. Keycloak: SPNEGO is disabled by default. In the browser flow set *Kerberos* from disabled to alternative (optional) or required. Then configure User Federation: for an LDAP backed Kerberos, toggle *Allow Kerberos authentication* on the LDAP provider; otherwise add a *Kerberos* user storage provider. The Kerberos provider imports simple principal information only; first name, last name and email are not provisioned.
4. Clients: need a Kerberos client with the same `krb5.conf` and SPNEGO enabled in the browser (Firefox: put `.mydomain.org` in `network.negotiate-auth.trusted-uris`). Windows domain clients need no change.

Warning from the docs: the Negotiate scheme allows NTLM fallback and some Windows browsers support NTLM by default, so users may see an NTLM dialog that they must cancel because Keycloak does not support it. Credential delegation is deprecated and has security implications.

Troubleshooting from the docs: enable the Debug flag on the Kerberos or LDAP provider, TRACE logging for category `org.keycloak`, and the system properties `-Dsun.security.krb5.debug=true -Dsun.security.spnego.debug=true`.

## Checked
2026-11-03. Confirmed against server_admin/topics/authentication/kerberos.adoc. Removed (not on the page): clock skew and SPN-mismatch gotchas, the `kinit`/LOGIN event Verify step and the "restricted path" aside.
Method: documentation only; no commands were run.
