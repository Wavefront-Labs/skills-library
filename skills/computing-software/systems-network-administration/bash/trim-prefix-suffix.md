---
id: computing-software.systems-network-administration.bash.trim-prefix-suffix
name: trim-prefix-suffix
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, trim-prefix-suffix, strip-suffix, shell-scripting]
level: practitioner
status: docs-checked
description: "Strip prefixes and suffixes with bash ${var#pat}, ##, % and %% for extensions, basenames and path pieces."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trimming with # ## % %%
**Goal:** cut text from the start or end without forking.
```bash
f=/var/log/app.tar.gz
echo "${f##*/}"   # app.tar.gz   (basename)
echo "${f%/*}"    # /var/log     (dirname)
echo "${f%.*}"    # /var/log/app.tar     (shortest suffix)
echo "${f%%.*}"   # /var/log/app         (longest suffix)
echo "${f#*/}"    # var/log/app.tar.gz   (shortest prefix)
echo "${f%.gz}.bz2"
```
- `#` and `%` remove the SHORTEST matching pattern (from the start / the end), `##` and `%%` the LONGEST.
- The word is expanded to a pattern (a glob, see Pattern Matching), not a regex.
- On `@` or `*`, or an array subscripted with them, the removal applies to each member in turn.
- If the pattern does not match, the value is unchanged.
- Self-check: `x=a.b.c; [[ ${x%.*} == a.b && ${x%%.*} == a ]]`.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual, Shell Parameter Expansion. Confirmed the four operators, shortest versus longest, glob patterns and per-member application. Removed the keyboard mnemonic, the POSIX-portability claim and the quoted-variable pattern advice, which were not confirmed in the pages read.
