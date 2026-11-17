---
id: computing-software.software-engineering.nim.strscans-and-parseutils
name: strscans-and-parseutils
category: computing-software
field: software-engineering
product: nim
tags: [strscans-and-parseutils, stdlib-strutils-text, scanf, scanp, strscans, parseutils, parser, tokenizing, nim]
level: advanced
status: docs-checked
description: "Parse structured lines with the scanf macro from strscans and incremental parseutils helpers."
sources:
  - https://nim-lang.org/docs/strscans.html
  - https://nim-lang.org/docs/parseutils.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scanf, scanp and parseutils for structured text

Goal: parse text without regex.

```nim
import std/strscans
var name: string; var age: int
if scanf("bob 42", "$w $i", name, age): echo name, age
```
- Patterns: `$i` decimal integer, `$f` float, `$w` ASCII identifier, `$s` skips optional whitespace, `$+` at least one character up to the next token, `$*` possibly empty match up to the next token, `$.` end of input, `${proc}` user matcher; other text matches verbatim. `scanf` returns true when the input starts with the pattern.
- `scanp` offers a PEG-like pattern syntax with captures for more complex grammars.
- `parseutils`: `parseUntil(s, token, ' ', start)`, `skipWhitespace`, `parseWhile` return characters consumed so you can walk a buffer index.

Gotchas:
- No backtracking: if the match fails after a value was bound, that variable is not restored.
- Add `$.` to the pattern to require that nothing is left over.

Verify: the sample above prints bob42 (`echo` puts no space between its arguments).

## Checked

2026-11-03. Confirmed against the strscans and parseutils pages: `$i $f $w $s $* $+ $. ${foo}` semantics, scanf prefix-match behaviour and no backtracking, parseUntil, parseWhile, skipWhitespace. Real error fixed: the Verify line said the sample prints `bob 42`; `echo name, age` prints `bob42`. Removed: speed claims and the capture-type claim.

Method: documentation only; no commands were run.
