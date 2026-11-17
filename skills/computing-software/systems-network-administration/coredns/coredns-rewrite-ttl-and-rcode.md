---
id: computing-software.systems-network-administration.coredns.coredns-rewrite-ttl-and-rcode
name: coredns-rewrite-ttl-and-rcode
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, rewrite, ttl, rcode, response]
level: practitioner
status: docs-checked
description: "Adjust response TTLs with single values or MIN-MAX ranges and change response codes such as SERVFAIL to NOERROR with rewrite."
sources:
  - https://coredns.io/plugins/rewrite/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune cacheability and mask unwanted response codes.

TTL syntax: `rewrite [continue|stop] ttl [exact|prefix|suffix|substring|regex] STRING [SECONDS|MIN-MAX]`. An omitted match type defaults to exact.

```
rewrite continue {
    ttl regex (.*)\.coredns\.rocks 15
}
rewrite ttl example.com. 30-300
rewrite ttl example.com. -30
rewrite ttl example.com. 30-
rewrite ttl example.com. 30
```

A range clamps the TTL: below MIN it is set to MIN, above MAX it is set to MAX, inside the range it is unchanged. Ranges may be unbounded on one side: `-30` equals `0-30`, and `30` equals `30-30`. Use a low value to prevent or limit caching, or raise 0 so a downstream cache stores it.

RCODE syntax: `rewrite [continue|stop] rcode [match-type] STRING FROM TO`. FROM and TO are text or numeric values: 0 NOERROR, 1 FORMERR, 2 SERVFAIL, 3 NXDOMAIN, 4 NOTIMP, 5 REFUSED, 6 YXDOMAIN, 9 NOTAUTH and others up to 23 BADCOOKIE.

```
rewrite continue {
    rcode regex (.*)\.coredns\.rocks SERVFAIL NOERROR
}
rewrite continue {
    rcode regex (.*)\.coredns\.rocks 2 0
}
```

Both forms are equivalent.

## Checked

2026-11-08. Checked in full against the rewrite plugin README. TTL ranges and RCODE table match; no changes needed beyond promotion.

Method: documentation only; no commands were run.
