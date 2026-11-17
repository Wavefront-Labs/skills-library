---
id: computing-software.systems-network-administration.bash.brace-sequence-expansion
name: brace-sequence-expansion
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, brace-sequence-expansion, brace-padding, shell-scripting]
level: practitioner
status: docs-checked
description: "Generate sequences and padded numbers with bash brace expansion {1..10}, {01..10}, steps and nested lists."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brace sequences and padding
**Goal:** produce lists without seq or loops.
```bash
echo {1..5}          # 1 2 3 4 5
echo {01..10}        # zero padded
echo {a..e} {10..0..5}
mkdir -p proj/{src,test,docs}/{a,b}
cp file.conf{,.bak}  # cp file.conf file.conf.bak
echo {1..3}{a,b}
```
- Expansion happens BEFORE variable expansion: `{1..$n}` does not work. Use `seq 1 "$n"` or `for ((i=1;i<=n;i++))`.
- Step form is `{start..end..step}`; if either endpoint begins with a zero every term is zero-padded to the same width.
- A brace expansion needs unquoted braces and at least one unquoted comma or a valid sequence expression; otherwise it is left unchanged (so `{a}` is literal).
- Historic `sh` does not treat braces specially, so `file{1,2}` stays literal there; `set +B` turns brace expansion off in bash.
- Self-check: `[ "$(echo {a,b}x)" = "ax bx" ]`.

## Checked

2026-11-02: Confirmed in Brace Expansion (strictly textual and done before other expansions, sequence form `x..y[..incr]`, zero padding, incorrectly formed expansions left unchanged, sh incompatibility, `+B`). Removed: bash 4 version claim, dash claim.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
