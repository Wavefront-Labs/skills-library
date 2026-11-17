---
id: computing-software.systems-network-administration.dns-dhcp.gss-tsig-with-active-directory
name: gss-tsig-with-active-directory
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dynamic-dns, gss-tsig, kerberos, active-directory, bind, tkey-gssapi-keytab, secure-dynamic-update]
level: practitioner
status: docs-checked
description: "Accept secure dynamic updates from Windows clients and DCs on BIND with GSS-TSIG: SPN and keytab, tkey-gssapi-keytab, ms-self update-policy."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-tkey-gssapi-keytab
  - https://www.rfc-editor.org/rfc/rfc3645
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GSS-TSIG with Active Directory

Windows clients send "secure dynamic updates" authenticated with Kerberos through GSS-TSIG (RFC 3645: TSIG keys established with TKEY using GSS-API), not shared TSIG keys. BIND can accept them when it hosts the zone.

## 1. Service principal and keytab (practitioner advice)
Create a Kerberos service principal for the BIND host in the AD realm (a DNS/host principal for the server name), export it to a keytab with the AD tooling you use (for example ktpass), and copy the keytab to the BIND server readable only by the named user. Use an AES enctype on the account. The exact commands vary with the AD functional level; they are not covered by the BIND documentation.

## 2. BIND
```
options {
    tkey-gssapi-keytab "/etc/bind/dns.keytab";
};
zone "corp.example.net" {
    type primary;
    file "dynamic/corp.example.net.db";
    update-policy {
        grant CORP.EXAMPLE.NET ms-self . A AAAA;
    };
};
```
- `tkey-gssapi-keytab` sets the Kerberos keytab file used for GSS-TSIG updates.
- Per the BIND reference, `grant EXAMPLE.COM ms-self . A AAAA` lets any machine with a valid principal in that realm update its own address records.
- `ms-selfsub` also allows updates to any subdomain of the machine's name. `ms-subdomain` allows updates at or below a named domain for any machine in the realm. `ms-subdomain-self-rhs` adds the restriction that PTR and SRV target names must match the machine named in the principal.
- Tighten or extend the rules to match the records your DCs and servers need to register (for example SRV records); the ruletypes above are the documented building blocks.
- Kerberos needs a valid realm configuration on the BIND host and clocks reasonably in sync with the KDCs (practitioner advice; use NTP).

## Gotchas
- `ms-self` is for Windows machine principals, where the machine part is an unqualified name; `krb5-self` is for Kerberos principals such as `host/machine@REALM` whose machine part is an absolute name. The two are similar but not identical (BIND reference).
- DHCP servers that update on behalf of clients need their own principal granted in update-policy (practitioner advice).

## Verify
- [ ] A domain-joined client re-registers its address (for example `ipconfig /registerdns`) and the record appears; the denied case (a different machine updating that name) is refused.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the BIND 9 reference page (tkey-gssapi-keytab, update-policy ruletypes ms-self/ms-selfsub/ms-subdomain/ms-subdomain-self-rhs/krb5-self) and skimmed RFC 3645 (GSS-TSIG with TKEY). Removed as unsupported: the New-ADUser, setspn and ktpass commands and flags, the DC wildcard grant, the 5-minute clock figure, nsupdate -g test with its expected log line, the event IDs 8019/8020 and the Kea D2 claim.
