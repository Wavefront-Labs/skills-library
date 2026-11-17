---
id: computing-software.systems-network-administration.dns-dhcp.soa-and-ns-records-at-the-apex
name: soa-and-ns-records-at-the-apex
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, soa-record, ns-record, zone-apex, serial-number]
level: practitioner
status: verified
description: "Get the SOA and NS records at a zone apex right: serial formats, refresh/retry/expire/minimum values, MNAME/RNAME, NS consistency and TTL choices."
sources:
  - https://www.rfc-editor.org/rfc/rfc1035#section-3.3.13
  - https://www.rfc-editor.org/rfc/rfc2308
  - https://www.ripe.net/publications/docs/ripe-203
  - https://www.rfc-editor.org/rfc/rfc1982
  - https://www.rfc-editor.org/rfc/rfc2136
  - https://www.rfc-editor.org/rfc/rfc2182
  - https://www.rfc-editor.org/rfc/rfc1996
  - https://www.rfc-editor.org/rfc/rfc1034
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SOA and NS records at the apex

Every zone has exactly one SOA and at least two NS records at its apex.

## SOA fields
```
example.com. 3600 IN SOA ns1.example.com. hostmaster.example.com. (
        2026101801 ; serial  YYYYMMDDnn
        7200       ; refresh: secondaries check this often
        3600       ; retry: after a failed refresh
        1209600    ; expire: secondaries stop answering after 2 weeks without contact
        3600 )     ; minimum: negative caching TTL (RFC 2308)
```
| Field | Notes |
|-------|-------|
| MNAME | primary master name; RFC 2136 update requesters try the primary named by the SOA MNAME first; can be a hidden primary |
| RNAME | contact mailbox with the `@` as a dot; escape dots in the local part (`john\.doe.example.com.`) |
| Serial | must increase on every change or secondaries never transfer; date format or unixtime |
| Expire | longer than any realistic primary outage; too short makes secondaries go dark |
| Minimum | negative cache TTL; 300-3600 s; large values make new names slow to appear after NXDOMAIN |
RIPE-203 (its example serial is 1999022301, so it is an old document) recommends refresh 86400, retry
7200, expire 3600000 and minimum 172800 for stable zones. Its 2-day minimum is far above the 300-3600 s
in the table above, and the minimum is the negative-caching TTL (RFC 2308), so treat those values as
historical. With NOTIFY (RFC 1996) secondaries are told about changes promptly, which makes refresh
mostly a fallback.

## Serial gotchas
- Going backwards (e.g. from 2026101801 to 20261019, fewer digits) breaks transfers: under RFC 1982
  serial arithmetic 20261019 is "before" 2026101801 (computed), so secondaries keep their copy. Fix it
  by walking the serial up in steps of at most 2^31 - 1 (adding 2^31 or more is undefined in RFC 1982;
  2026101801 + 2^31 - 1 compares as after the old value) until it passes the old value, or reload all
  secondaries manually.
- Dynamic and inline-signed zones are bumped by the server; BIND's `serial-update-method` (`increment`,
  `date` or `unixtime`) controls how.

## NS at the apex
- At least two servers on different networks (RFC 2182 section 5: the DNS specification and registration
  rules require at least two, and it advises more than two listed servers).
- The apex NS set should match the parent's delegation NS set; a mismatch gives inconsistent answers
  and lame delegations.
- No CNAME at the apex (it would conflict with SOA/NS; RFC 1034: where a CNAME exists no other data
  should); use ALIAS/flattening provider features.

## Check
```
dig example.com SOA +multiline
dig +nssearch example.com            # SOA serial from each listed NS
```

## Verify
- [ ] All authoritative servers report the same serial after a change, and NS sets match the parent.
