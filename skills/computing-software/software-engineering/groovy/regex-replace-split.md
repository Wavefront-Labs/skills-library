---
id: computing-software.software-engineering.groovy.regex-replace-split
name: regex-replace-split
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, regex-replace-split]
level: practitioner
status: draft
description: "replaceAll with closures, replaceFirst, split, findAll and eachMatch on strings in Groovy."
sources:
  - https://groovy-lang.org/operators.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replace, split and each-match
```groovy
assert 'a1b22'.replaceAll(/\d+/) { m -> "<$m>" } == 'a<1>b<22>'
assert 'a1b22'.findAll(/\d+/) == ['1', '22']
assert 'k=v'.split('=') == ['k', 'v']
'x1y2'.eachMatch(/\d/) { println it }
assert 'ab' ==~ /(?i)AB/       // flags inline
```
- `replaceAll(Pattern/String, Closure)` passes the match (a `String` or list of groups when the pattern has groups).
- Java `\Q..\E` and `Pattern.quote` for literal text.

## Gotchas
- `String.split` takes a regex, so `'a.b'.split('.')` returns an empty array; use `split(/\./)`.
- In single-quoted strings backslashes need doubling; use slashy strings.

## Self-check
Run the snippet.
