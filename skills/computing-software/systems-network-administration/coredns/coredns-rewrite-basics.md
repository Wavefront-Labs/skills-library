---
id: computing-software.systems-network-administration.coredns.coredns-rewrite-basics
name: coredns-rewrite-basics
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, rewrite, continue, stop, fields]
level: practitioner
status: docs-checked
description: "Rewrite queries and responses invisibly with the rewrite plugin: syntax, fields, and how continue and stop chain multiple rules."
sources:
  - https://coredns.io/plugins/rewrite/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change parts of a DNS message before or after later plugins.

Syntax: `rewrite [continue|stop] FIELD [TYPE] [(FROM TO)|TTL] [OPTIONS]`.

Fields:
- `type`: query type, e.g. `rewrite type ANY HINFO`.
- `name`: query name (exact match by default).
- `class`: e.g. `rewrite class CH IN`.
- `edns0`: append an EDNS0 option.
- `ttl`, `cname`, `rcode`: rewrite parts of the response.

Rewrites are invisible to the client. Simple rewrites are fast; complex (regex) ones are slower.

Multiple rules: `continue` applies the next rule after a match; `stop` makes the current rule the last. The default is stop. Requests are rewritten in configuration line order, while response rewrites (the answer option) run in reverse order.

The block form groups a rule:

```
rewrite stop {
    name regex (.*)-(us-west-1)\.coredns\.rocks {1}.service.{2}.consul
    answer name (.*)\.service\.(us-west-1)\.consul {1}-{2}.coredns.rocks
}
```

The match type for `name` and `ttl` is optional and defaults to exact; if OPTIONS are given the type must be written. Fields: `class` rewrites the message class (IN, CH, HS), `ttl` and `rcode` rewrite the response, `cname` rewrites the CNAME target of the response.

Failure mode: if a rewritten name is not a legal domain name, the plugin returns an error to the client.

## Checked

2026-11-08. Checked in full against the rewrite plugin README. Replaced an invalid block example (answer auto on its own line) with the documented answer name form, removed an unsupported claim about restoring the question section, and added match-type defaults and field notes.

Method: documentation only; no commands were run.
