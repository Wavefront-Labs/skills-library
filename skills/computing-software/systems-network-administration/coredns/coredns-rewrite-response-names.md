---
id: computing-software.systems-network-administration.coredns.coredns-rewrite-response-names
name: coredns-rewrite-response-names
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, rewrite, answer-auto, answer-name, answer-value]
level: advanced
status: docs-checked
description: "Make rewritten answers match the original question with answer auto, answer name and answer value options."
sources:
  - https://coredns.io/plugins/rewrite/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid question and answer mismatches after a name rewrite.

Three ways exist to rewrite the answer section:
- `answer auto`: best effort. Any occurrence of the rewritten question in the answer is mapped back. Exact-type rewrites are always rewritten. For a suffix rule, auto exchanges FROM and TO.
- `answer name FROM TO`: regex-based rewrite of the answer's owner names.
- `answer value FROM TO`: regex rewrite of record values; applies to names returned by CNAME, DNAME, SOA, SRV, MX, NAPTR, NS and PTR. Names in the authority and additional sections are rewritten too.

Examples:

```
rewrite stop {
    name suffix .coredns.rocks .service.consul answer auto
}
rewrite stop {
    name regex (.*)-(us-west-1)\.coredns\.rocks {1}.service.{2}.consul
    answer name (.*)\.service\.(us-west-1)\.consul {1}-{2}.coredns.rocks
}
```

Syntax is strict: for response rewrites only name rules may match the question, and the answer rule must come after the name rule. Several answer options can be chained; the keyword `answer` may be omitted after the first:

`rewrite [continue|stop] name regex FROM TO answer name FROM TO [answer] value FROM TO`

Response rewrites run in reverse order of the request rules.

## Checked

2026-11-08. Checked in full against the rewrite plugin README. answer auto, answer name, answer value, strict syntax and reverse ordering match; no changes needed beyond promotion.

Method: documentation only; no commands were run.
