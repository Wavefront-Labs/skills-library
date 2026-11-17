---
id: computing-software.software-engineering.groovy.triple-quoted-slashy
name: triple-quoted-slashy
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, triple-quoted-slashy]
level: practitioner
status: docs-checked
description: "Multiline strings, stripIndent, slashy strings for regexes and dollar-slashy for text containing slashes."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-syntax.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triple-quoted, slashy and dollar-slashy strings
- `'''...'''` plain multiline; `"""...${x}..."""` interpolating. Put `\` right after the opening quotes to skip the first newline.
- `.stripIndent()` removes common leading whitespace; `.stripMargin()` takes a delimiter character that marks where the text starts.
- Slashy `/\d+\.\d+/` needs no backslash doubling and interpolates `$x`. It cannot be empty (`//` is a comment).
- Dollar-slashy `$/ ... /$` allows `/` freely; escape `$` as `$$` and `/` as `$/`.
```groovy
def re = ~/\d{3}-\d{4}/
def doc = """\
  line1
  line2""".stripIndent()
assert doc == "line1\nline2"
```

## Gotchas
- A slashy string cannot end with a backslash before the closing slash.

## Self-check
Run the snippet; the assert holds.

## Checked

2026-11-02. Confirmed against the Syntax chapter (triple-quoted, slashy and dollar-slashy strings and their escaping rules). Removed: the line-ending claim.

Method: documentation only; no commands were run.
