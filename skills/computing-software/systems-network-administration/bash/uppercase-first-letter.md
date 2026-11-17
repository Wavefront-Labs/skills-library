---
id: computing-software.systems-network-administration.bash.uppercase-first-letter
name: uppercase-first-letter
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, uppercase-first-letter, capitalize, shell-scripting]
level: intro
status: docs-checked
description: "Capitalise the first letter or each word of a string in bash with ${var^}, ${var^^} and a loop, without forking."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capitalising the first letter
**Goal:** title-case text natively.
```bash
s="hello world"
echo "${s^}"            # Hello world
echo "${s^^}"           # HELLO WORLD
echo "${s^^[aeiou]}"    # hEllO wOrld  (pattern restricts which chars)
for w in $s; do printf '%s ' "${w^}"; done; echo      # each word
name="mcDONALD"; echo "${name,,}" ; echo "${name^}"
```
- `^` converts the first character to upper case if it matches the pattern, `^^` every matching character; `,` and `,,` do the same to lower case. An omitted pattern acts like `?` (matches every character); the pattern must not try to match more than one character.
- On `@` or `*`, or an array subscripted with them, the conversion applies to each member in turn.
- `${var@u}` upper-cases the first character and `${var@U}` all of them; `${var@L}` lower-cases all.
- Unquoted `for w in $s` is subject to word splitting and filename expansion; consider `set -f` first.
- Self-check: `x=abc; [ "${x^}" = Abc ]`.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual, Shell Parameter Expansion. Confirmed the `^`, `^^`, `,`, `,,` forms, optional pattern, per-member application and the `@U`, `@u`, `@L` transformations. Removed the bash 4.0 and macOS 3.2 version claims, the locale claim and the tr/awk/sed alternatives, which were not confirmed in the pages read.
