---
id: computing-software.systems-network-administration.openldap.ldap-conf-client
name: ldap-conf-client
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, ldap-conf, ldaprc, client-defaults, uri, base, sasl-secprops]
level: intro
status: docs-checked
description: "Set OpenLDAP client defaults in ldap.conf and .ldaprc: URI, BASE, BINDDN, limits, SASL and TLS options, file precedence and LDAP environment variables."
sources:
  - https://www.openldap.org/software/man.cgi?query=ldap.conf&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ldap.conf client configuration
Example:
```
URI ldap://ldap.example.com ldap://ldap2.example.com
BASE dc=example,dc=com
TLS_CACERT /path/to/ca.pem
SASL_MECH GSSAPI
```
Options: `URI` (ports 389 ldap, 636 ldaps), `BASE`, `BINDDN` (user-only), `DEREF never|searching|finding|always` (default never), `SIZELIMIT`, `TIMELIMIT` (0 unlimited), `REFERRALS` (default on), `NETWORK_TIMEOUT`, `TIMEOUT`, `SOCKET_BIND_ADDRESSES`, `KEEPALIVE_*` (Linux), `VERSION`.
SASL: `SASL_MECH`, `SASL_REALM`, `SASL_AUTHCID`, `SASL_AUTHZID` (user-only), `SASL_SECPROPS` (default `noanonymous,noplain`, `minssf` 0, `maxbufsize` 65536), `SASL_NOCANON`, `SASL_CBINDING`. GSSAPI: `GSSAPI_SIGN`, `GSSAPI_ENCRYPT`, `GSSAPI_ALLOW_REMOTE_PRINCIPAL`.
TLS: `TLS_CACERT`, `TLS_CACERTDIR`, `TLS_CERT`/`TLS_KEY` (user-only), `TLS_REQCERT` (default demand), `TLS_REQSAN` (allow), `TLS_CIPHER_SUITE`, `TLS_PROTOCOL_MIN`, `TLS_CRLCHECK`.

Files, read in order, later overriding earlier:
1. System `/usr/local/etc/openldap/ldap.conf`
2. User `~/ldaprc`, `~/.ldaprc`, `./ldaprc`
3. System file named by `LDAPCONF`
4. User files named by `LDAPRC` (`$HOME/$LDAPRC`, `$HOME/.$LDAPRC`, `./$LDAPRC`)
5. Environment `LDAP<OPTION>`, such as `LDAPBASE`

`LDAPNOINIT` disables all defaulting. User-only options are ignored in the system file; tools such as ldapsearch accept `-o opt[=optparam]` for any ldap.conf option.

## Checked

2026-11-04. Confirmed against the OpenLDAP 2.6 ldap.conf(5) manual page: option names and defaults (DEREF never, REFERRALS on, SASL_SECPROPS defaults, minssf 0, maxbufsize 65536, TLS_REQCERT demand, TLS_REQSAN allow), ports 389/636, user-only options, Linux-only KEEPALIVE_* options, file read order, LDAPNOINIT, LDAPCONF, LDAPRC and LDAP<option> variables. The -o opt[=optparam] option is confirmed on the ldapsearch(1) page. Removed the unconfirmed -o option=value form.

Method: documentation only; no commands were run.
