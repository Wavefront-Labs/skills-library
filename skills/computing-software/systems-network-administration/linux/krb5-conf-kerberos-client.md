---
id: computing-software.systems-network-administration.linux.krb5-conf-kerberos-client
name: krb5-conf-kerberos-client
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kerberos, krb5-conf, mit-kerberos, kinit, klist, keytab, ktutil, realm, kdc, dns-lookup-kdc, credential-cache, active-directory, sysadmin]
level: practitioner
status: docs-checked
description: "Configure the Kerberos client in /etc/krb5.conf: realms, KDC discovery, domain_realm mapping, ticket lifetimes, cache types, keytabs, and debugging kinit failures with KRB5_TRACE."
sources:
  - https://web.mit.edu/kerberos/krb5-latest/doc/admin/conf_files/krb5_conf.html
  - https://web.mit.edu/kerberos/krb5-latest/doc/user/user_commands/kinit.html
  - https://web.mit.edu/kerberos/krb5-latest/doc/admin/troubleshoot.html
  - https://web.mit.edu/kerberos/krb5-latest/doc/basic/ccache_def.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# krb5.conf — the Kerberos client

**Goal:** `kinit` works for users and services against AD or FreeIPA, hosts map to the
right realm, and Kerberos failures can be explained from a trace.

## 1. A typical krb5.conf
```ini
# /etc/krb5.conf
includedir /etc/krb5.conf.d/          # include every file in that directory (absolute path, must exist)

[libdefaults]
    default_realm = CORP.EXAMPLE
    dns_lookup_kdc = true             # find KDCs via _kerberos._udp/_tcp SRV records
    dns_lookup_realm = false
    rdns = false                       # no reverse lookups when canonicalising host names
    dns_canonicalize_hostname = fallback
    ticket_lifetime = 10h
    renew_lifetime = 7d
    forwardable = true
    default_ccache_name = KEYRING:persistent:%{uid}   # cache types: FILE, DIR, KEYRING, KCM (see the ccache page)
    udp_preference_limit = 0           # try TCP before UDP for messages above this size (0 = always)

[realms]
    CORP.EXAMPLE = {
        kdc = dc1.corp.example        # optional when SRV records exist
        kdc = dc2.corp.example
        admin_server = dc1.corp.example
    }

[domain_realm]
    .corp.example = CORP.EXAMPLE
    corp.example = CORP.EXAMPLE
    .lab.example = CORP.EXAMPLE
```
Realm names are UPPERCASE by convention and case-sensitive.

## 2. Users
```bash
kinit alice                    # alice@CORP.EXAMPLE
klist                          # cache, principal, tickets, expiry, flags (F forwardable, R renewable)
kinit -R                       # renew
kvno HTTP/web01.corp.example   # acquire a service ticket and print its key version number
kdestroy -A
```

## 3. Keytabs (services, scripts)
```bash
klist -kte /etc/krb5.keytab                 # principals, KVNO, enctypes
kinit -kt /etc/krb5.keytab 'WEB01$@CORP.EXAMPLE'
```
Keytabs are passwords: `chmod 600`, owned by the service account.

## 4. Debug
```bash
KRB5_TRACE=/dev/stdout kinit alice
```
| Error | Usual cause |
|---|---|
| Clock skew | the `clockskew` relation tolerates 300 seconds (5 minutes) by default; fix time synchronisation |
| `KDC has no support for encryption type` | listed under frequently seen errors in the MIT troubleshooting page; compare the enctypes the client and the account allow |
| `Preauthentication failed` | can be caused by an expired KDC certificate when PKINIT is used |

## Gotchas
- Credential cache types differ in behaviour: a script that expects a `FILE:` cache breaks if the default is `KEYRING:` or `KCM:`; set `KRB5CCNAME` for such scripts.
- Programs that use secure library contexts (setuid programs, parts of login) may ignore `KRB5_TRACE`.

## Verify
- [ ] `kinit user && klist` shows a TGT for the right realm; `kvno` for a known service succeeds.
- [ ] `kinit -kt /etc/krb5.keytab <host principal>` works; `KRB5_TRACE` shows KDCs found via the intended method.

## Checked

Documentation check. Checked 2026-10-27 against the MIT Kerberos documentation (krb5-latest: krb5.conf, kinit, klist, kdestroy, kvno, ccache and troubleshooting pages, web.mit.edu): `default_realm`, `dns_lookup_kdc` (SRV records), `dns_lookup_realm` (TXT records), `rdns`, `dns_canonicalize_hostname`, `ticket_lifetime` (default 1 day), `renew_lifetime` (default 0), `forwardable` (default false), `default_ccache_name` with `%{uid}`, the `KEYRING:persistent:uidnumber` and `FILE` cache forms, `udp_preference_limit`, `includedir`, `clockskew` (300 s), `kinit -R` and `-k -t keytab`, `kdestroy -A`, `klist -k -e -t`, `kvno`, and `KRB5_TRACE`. Removed the vendor-specific crypto-policy, SSSD and realmd remarks, the other error strings the pages do not list, the ktutil remark and the AD PAC claim.
Method: documentation only; no commands were run.
