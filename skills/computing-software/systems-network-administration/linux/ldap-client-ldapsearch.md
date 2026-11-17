---
id: computing-software.systems-network-administration.linux.ldap-client-ldapsearch
name: ldap-client-ldapsearch
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ldap, ldap-client, ldapsearch, openldap-clients, ldap-conf, ldaps, starttls, sasl-gssapi, active-directory, freeipa, directory-lookup, sysadmin]
level: practitioner
status: docs-checked
description: "Query LDAP and Active Directory from Linux with ldapsearch: ldap.conf defaults, simple vs GSSAPI binds, LDAPS/StartTLS with CA trust, search filters, paging, and decoding results."
sources:
  - https://www.openldap.org/software/man.cgi?query=ldapsearch
  - https://www.openldap.org/software/man.cgi?query=ldap.conf
  - https://datatracker.ietf.org/doc/html/rfc4515
  - https://learn.microsoft.com/en-us/windows/win32/adsi/search-filter-syntax
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/useraccountcontrol-manipulate-account-properties
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LDAP client and ldapsearch

**Goal:** prove what the directory says about a user or group — independently of SSSD — and
debug binds, TLS and filters.

## 1. Install and defaults
```bash
# install your distribution's OpenLDAP client tools (ldapsearch, ldapwhoami)
```
```
# ldap.conf in the system configuration directory (ETCDIR, set when the package is built)
URI     ldaps://dc1.corp.example ldaps://dc2.corp.example
BASE    dc=corp,dc=example
TLS_CACERT /path/to/ca.pem                      # CA certificates the client will recognise
TLS_REQCERT demand
SASL_NOCANON on                                  # no reverse-DNS canonicalisation of SASL host names (default off)
```
Per-user overrides go in `.ldaprc` in the home directory (see ldap.conf(5)).

## 2. Binds
```bash
ldapsearch -x -H ldaps://dc1.corp.example -b dc=corp,dc=example '(uid=alice)'          # anonymous (often disabled)
ldapsearch -x -D 'svc-ldap@corp.example' -W '(sAMAccountName=alice)'                    # simple bind, prompts
ldapsearch -x -D 'cn=svc,ou=services,dc=corp,dc=example' -y ./ldap-pass '(uid=alice)'   # complete file contents are the password (no trailing newline)
kinit alice && ldapsearch -Y GSSAPI -H ldap://dc1.corp.example '(sAMAccountName=alice)'  # Kerberos, no password on the wire
ldapsearch -x -ZZ -H ldap://ldap.corp.example ...                                        # StartTLS required
ldapwhoami -x -D ... -W                                                                  # test a bind only
```
Never simple-bind over plain `ldap://` without `-ZZ` — the password crosses the network in clear.

## 3. Useful searches
```bash
ldapsearch -LLL ... '(&(objectClass=user)(sAMAccountName=alice))' memberOf userAccountControl pwdLastSet
ldapsearch -LLL ... '(&(objectClass=group)(cn=linux-admins))' member
ldapsearch -LLL ... '(memberOf:1.2.840.113556.1.4.1941:=cn=linux-admins,ou=groups,dc=corp,dc=example)' sAMAccountName   # AD nested groups
ldapsearch -LLL ... '(&(objectClass=posixAccount)(uidNumber=10042))' uid
ldapsearch -LLL -E pr=500/noprompt ... '(objectClass=user)' dn      # paged results
ldapsearch -LLL -s base -b '' '+' supportedSASLMechanisms namingContexts    # Root DSE
```
Results use an extended LDIF; option `-L` controls the output format.
Filter syntax: `&`, `|`, `!`, wildcard `*`; escape `( ) * \` in values as `\28 \29 \2a \5c`.

## Gotchas
- `Can't contact LDAP server` with ldaps:// is usually TLS trust (add `-d 1` for debug output, if the tool was built with debugging) or a blocked port.
- AD: `userAccountControl` flag `ACCOUNTDISABLE` (0x0002) marks a disabled account.
- `Size limit exceeded` is a server-side limit — use paged results.
- A wrong search base returns "No such object", not zero entries.

## Verify
- [ ] `ldapwhoami` with the service account succeeds over LDAPS/StartTLS with `TLS_REQCERT demand`.
- [ ] A user/group search returns the same membership that `id <user>` shows through SSSD.

## Checked

Documentation check. Checked 2026-10-27 against the OpenLDAP ldapsearch(1), ldap.conf(5) and ldapwhoami(1) pages (man7.org), RFC 4515, and Microsoft Learn pages on search filter syntax and userAccountControl: `-x`, `-D`, `-W`, `-y` (complete file contents), `-Y`, `-Z[Z]` (StartTLS required with `-ZZ`), `-H`, `-b`, `-s base`, `-d`, `-E pr=size/noprompt`, the `+` operational attribute selector, `ldap.conf` keywords `TLS_CACERT`, `TLS_REQCERT`, `SASL_NOCANON` (default off) and `.ldaprc`, the RFC 4515 escapes `\2a`, `\28`, `\29`, `\5c`, the AD matching rule 1.2.840.113556.1.4.1941 (in-chain) and `ACCOUNTDISABLE` 0x0002. Removed the per-distro config paths and package names, the AD 1000 per page figure, `pwdLastSet=0`, the numeric result codes, the base64 remark and the SSSD remark.
Method: documentation only; no commands were run.
