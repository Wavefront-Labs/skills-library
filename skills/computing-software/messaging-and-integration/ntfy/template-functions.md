---
id: computing-software.messaging-and-integration.ntfy.template-functions
name: template-functions
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, template, template-functions, sprig, go-template]
level: advanced
status: docs-checked
description: "Use the Sprig-based functions available in ntfy templates and avoid their documented traps (set, must, dateModify, and)."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish/template-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template functions

ntfy's template functions are based on the Sprig library. Categories: string (`trim`, `upper`, `replace`, `regexMatch`), string list (`join`, `splitList`, `sortAlpha`), integer and float math (`add`, `mul`, `max`, `randInt`, `maxf`, `minf`), date (`now`, `date`, `dateModify`, `toDate`), defaults (`default`, `empty`, `coalesce`, `toJSON`, `ternary`), encoding (`b64enc`, `b64dec`), lists, dicts, type conversion, path, flow control (`fail`), reflection, crypto (`sha256sum`), URL (`urlParse`, `urlJoin`).

```
trim "   hello    "
now | date "2006-01-02"
default "foo" .Bar
chunk 3 (list 1 2 3 4 5 6 7 8)
get $myDict "name1"
```

## Gotchas

- Path functions only manipulate strings; there is no filesystem access.
- Functions without a `must` prefix (such as `regexMatch`) panic on problems; `must` variants return an error to the template engine.
- `set` and `unset` return the dict; assign the result to `$_` to avoid stray output. Dict keys must be strings.
- Lists are immutable (`append` returns a new list); dicts are mutable.
- `dateModify` returns the date unmodified if the modification format is wrong.
- Go's template `and` does not short-circuit; `dig` traverses nested dicts and returns a default if a key is missing.
- `plural` handles only English rules, and 0 is plural.
- `fromJSON` returns an empty string on invalid JSON; `mustFromJSON` returns an error.

## Checked

2026-11-04. Checked against the template-functions page: Sprig basis, set/unset with $_, must variants, immutable lists, dateModify, and/dig, plural, path functions and fromJSON match.
Method: documentation only; no commands were run.
