---
id: computing-software.systems-network-administration.coredns.coredns-rewrite-name-matching
name: coredns-rewrite-name-matching
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, rewrite, name, regex, suffix]
level: practitioner
status: docs-checked
description: "Rewrite query names with exact, prefix, suffix, substring or regex matching, using capture groups such as {1} in the target."
sources:
  - https://coredns.io/plugins/rewrite/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: map one namespace to another.

Syntax: `rewrite [continue|stop] name [exact|prefix|suffix|substring|regex] STRING STRING [OPTIONS]`.

Match types:
- `exact` (default): whole name equals.
- `substring`: partial match.
- `prefix`: name begins with the string.
- `suffix`: name ends with the string.
- `regex`: matches a regular expression. Patterns must not exceed 10000 characters.

If options are given, the match type must be written explicitly.

Examples from the docs:

```
rewrite name substring service.us-west-1.example.org service.us-west-1.consul
rewrite name regex (.*)-(us-west-1)\.example\.org {1}.service.{2}.consul
rewrite name suffix .schmoogle.com. .google.com.
```

Thus `ftp.service.us-west-1.example.org` becomes `ftp.service.us-west-1.consul`, and `ftp-us-west-1.example.org` becomes `ftp.service.us-west-1.consul`. In regex targets `{1}`, `{2}` are capture groups.

Pitfall: the query's question section is rewritten, so the answer names no longer match the question. Some resolvers treat that mismatch as a man-in-the-middle attack. Fix it with answer options (see the response rewrite skill). Exact rules are rewritten back automatically.

Rule order matters when several rules can match one query: they apply in line order, `stop` (the default) ends the list, and `continue` carries on with the following rule.

## Checked

2026-11-08. Checked in full against the rewrite plugin README. Removed an unsupported performance claim about regex rules; match types, 10000 character regex limit and examples match.

Method: documentation only; no commands were run.
