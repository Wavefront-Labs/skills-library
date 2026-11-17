---
id: computing-software.devops-ci-cd.rundeck.node-filter-syntax
name: node-filter-syntax
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, node-filter, tag-filter, regex-match, exclude-nodes]
level: practitioner
status: docs-checked
description: "Write Rundeck node filter expressions: attribute pairs, regex values, exact lists, tag AND/OR, negation, and the repeated-attribute gotcha."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/11-node-filters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A filter is a sequence of `attributename: value` pairs. Negate with `!attributename: value`. A bare value with no attribute is matched against `nodename`. The result is the nodes that match all clauses.

A value can be:
- A regular expression, matching every node whose attribute fits, for example `www.*`.
- A comma-separated list, each an exact match: `web1,web2`.
- For the `tags` attribute, a comma list is OR and a `+` list is AND. `a+b` needs both tags; `a+b,x` means both a and b, or x.

Gotcha: repeating the same attribute concatenates values into a comma list and does not use regex.

```
name: web1 name: web2        # same as name: web1,web2 (no regex)
```

To combine regexes use alternation in one value: `anode.*|bnode.*`.

Examples:

```
mynode1 mynode2
mynode1 !nodename: mynode2
tags: www+prod hostname: dev1.example.com,dev2.example.com
```

The first selects the two named nodes, the second includes mynode1 and excludes mynode2, the third selects nodes tagged both www and prod with either hostname.

Verify in the job or Commands page node filter preview before running.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Node Filters: attributename: value pairs, negation with !, bare value matched against nodename, regex and exact comma list values, tags OR with commas and AND with +, all clauses must match, repeated attribute concatenation without regex, the alternation tip, and the three examples. Nothing removed.

Method: documentation only; no commands were run.
