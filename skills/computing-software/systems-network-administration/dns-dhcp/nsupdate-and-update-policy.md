---
id: computing-software.systems-network-administration.dns-dhcp.nsupdate-and-update-policy
name: nsupdate-and-update-policy
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, dynamic-dns, ddns, nsupdate, update-policy, allow-update, tsig, tsig-keygen, rfc2136, jnl, rndc-freeze, rndc-sync, acme-dns-01]
level: practitioner
status: docs-checked
description: "Make RFC 2136 dynamic updates to BIND safely: TSIG keys, fine-grained update-policy grants, nsupdate scripts, prerequisites, journals and freeze/thaw."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter6.html#dynamic-update
  - https://bind9.readthedocs.io/en/latest/manpages.html#nsupdate-dynamic-dns-update-utility
  - https://datatracker.ietf.org/doc/html/rfc2136
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nsupdate and update-policy

## Key and grants
Generate a TSIG key with `tsig-keygen` (it prints the key statement to include in `named.conf`
and in the key file `nsupdate -k` reads).
```
include "/etc/bind/keys/acme-key.conf";
include "/etc/bind/keys/dhcp-key.conf";
zone "example.org" {
    type primary;
    file "dynamic/example.org.db";
    update-policy {
        grant acme-key name _acme-challenge.www.example.org. TXT;     // one name, one type
        grant acme-key subdomain _acme-challenge.example.org. TXT;
        grant dhcp-key subdomain dyn.example.org. A AAAA DHCID;        // DHCP clients under dyn.
    };
};
```
Dynamic update is enabled by an `allow-update` or an `update-policy` clause in the zone
statement. Use `update-policy` to grant a key only the names and record types it needs. The
rule types in the configuration grammar include `name`, `subdomain`, `wildcard`, `self`,
`selfsub`, `selfwild`, `zonesub`, `krb5-self`, `ms-self`, `tcp-self`, `external` and
`6to4-self`; `update-policy local;` makes named configure a local key for `nsupdate -l`.

## nsupdate
```
nsupdate -k /etc/bind/keys/acme-key.conf <<'EOF'
server 10.0.0.10
zone example.org
update delete _acme-challenge.www.example.org. TXT
update add _acme-challenge.www.example.org. 60 TXT "token-value"
send
EOF
nsupdate -l      # local update using the key named configures for update-policy local
```
An update request holds zero or more prerequisites and zero or more updates; `send` (or a
blank line) transmits them as one request. Prerequisites such as `prereq nxdomain name` or
`prereq yxrrset name class type` make the update conditional.

## Journals and manual edits
Changes made by dynamic update are stored in the zone's journal, named by appending `.jnl` to
the zone file name; it is binary and should not be edited. To edit a dynamic zone by hand:
```
rndc freeze example.org     # disable updates; zone file gets the journal changes
vi dynamic/example.org.db   # edit the zone file (bump the serial)
rndc thaw example.org       # reload the zone and re-enable updates
rndc sync -clean example.org   # update the zone file from the journal without freezing, and remove the .jnl
```

## Verify
- [ ] An update with a restricted key on a name outside its grant is refused.
- [ ] Changes appear on secondaries after `send`.

## Checked
2026-11-01: confirmed against the BIND 9 Administrator Reference Manual (Dynamic Update: journal naming, freeze/thaw/sync -clean) and the BIND 9 nsupdate and named.conf man pages (prereq commands, update-policy grammar, `-l`, tsig-keygen). Removed: semantics of individual rule types, tsig-keygen flags, claims about what allow-update permits, ACME client specifics, error-message text, directory-permission remark.
Method: documentation only; no commands were run.
