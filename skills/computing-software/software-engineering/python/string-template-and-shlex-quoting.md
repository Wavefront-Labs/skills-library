---
id: computing-software.software-engineering.python.string-template-and-shlex-quoting
name: string-template-and-shlex-quoting
category: computing-software
field: software-engineering
product: python
tags: [python, py-text-processing, string-template-shlex, string-template, shlex-quote, shlex-split, shell-quoting, safe-substitution]
level: practitioner
status: docs-checked
description: "Use string.Template for user-editable placeholders and shlex.split/quote/join for command-line strings, including why POSIX quoting is not safe for Windows shells."
sources: ["https://docs.python.org/3/library/string.html#template-strings", "https://docs.python.org/3/library/shlex.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# string.Template and shlex

## string.Template: safe, simple placeholders
```python
from string import Template
t = Template("Hello $name, you owe ${amount}USD. Cost: $$5")
t.substitute(name="Ada", amount=12)       # KeyError if a name is missing
t.safe_substitute(name="Ada")             # leaves missing placeholders as-is
t.get_identifiers()                       # 3.11+: ['name', 'amount']
t.is_valid()                              # 3.11+: detects malformed placeholders
```
`Template` offers simpler substitution than `str.format`: placeholders are plain identifiers with no attribute access or format specs. Subclass with a different `delimiter` or `idpattern` for formats where `$` is common (e.g. shell scripts).

## shlex: tokenising and quoting command lines
```python
import shlex
shlex.split('git commit -m "fix: a b" --amend')    # ['git','commit','-m','fix: a b','--amend']  (POSIX rules)
shlex.quote("a b; rm -rf /")                         # "'a b; rm -rf /'"  for POSIX shells only
shlex.join(["ls", "my file", "$HOME"])               # "ls 'my file' '$HOME'"  (3.8+)
shlex.split(line, comments=True)                     # strip # comments
```
`shlex.shlex(..., punctuation_chars=True)` also splits `;`, `&&`, `|` into tokens (3.6+) for mini shells.

## Rules
- Prefer `subprocess.run([...list...])` and avoid building shell strings at all. If you must call a shell, quote every dynamic part with `shlex.quote`.
- `shlex.quote` is not guaranteed correct on non-POSIX shells or shells from other operating systems such as Windows; pass a list instead.
- Since 3.12 `shlex.split(None)` raises an exception.

## Gotchas
- `Template.substitute` raises `ValueError` on a stray `$` (escape it as `$$`) and `KeyError` on a missing name; `safe_substitute` leaves them in place, which also hides malformed templates.
- Do number formatting before substituting; placeholders take no format spec.

## Verify
- [ ] Round-trip test: `shlex.split(shlex.join(args)) == args` for arguments with spaces, quotes, `$`, unicode.
- [ ] A test passes `"; touch /tmp/pwned"` as data and confirms no command runs.

## Checked

- 2026-11-03: checked against the CPython docs `library/string.rst` (template strings) and `library/shlex.rst`: `substitute`/`safe_substitute`, `is_valid` and `get_identifiers` (3.11), `delimiter`/`idpattern`, `shlex.split` POSIX default and `comments`, `quote` Windows warning, `join` (3.8), `punctuation_chars` (3.6), `split(None)` change in 3.12.
- Removed: `list2cmdline`, tilde/glob/env expansion remark, the exact unterminated-quote message, str() conversion claim.

Method: documentation only; no commands were run.
