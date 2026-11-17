---
id: computing-software.systems-network-administration.bash.set-u-nounset
name: set-u-nounset
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, set-u-nounset, unbound-variable, shell-scripting]
level: practitioner
status: docs-checked
description: "Use bash set -u to fail on unset variables, with safe defaults for optional values and the @ and * exemptions."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# set -u and unset variables
**Goal:** catch typos in variable names.
```bash
set -u
echo "$undefined"           # error: unbound variable, non-interactive shell exits
echo "${opt-}"              # default to empty, no error
echo "${1:?usage: $0 file}" # abort with message if $1 unset or empty
[[ -n ${DEBUG-} ]] && set -x
arr=(); echo "${arr[@]}"    # array subscripted with @ or * is exempt from -u
```
- `set -u` (same as `set -o nounset`) treats unset variables as an error during parameter expansion; the special parameters `@` and `*`, and arrays subscripted with `@` or `*`, are exempt. A non-interactive shell exits.
- `${v:?msg}` writes msg to stderr and exits a non-interactive shell when v is unset or null; an interactive shell does not exit. Without the colon (`${v?msg}`) only unset triggers it.
- `${v:=x}` assigns x when v is unset or null (positional and special parameters cannot be assigned this way). `${v-d}` tests only unset; `${v:-d}` also treats null as unset.
- Typo-catching only helps if variable names are spelled consistently.
- Self-check: `bash -uc 'echo $nope'` exits non-zero.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (The Set Builtin, Shell Parameter Expansion). Confirmed `-u` semantics and the `@`/`*` exemption, `:?`, `:=`, `-` and `:-` behaviour. Removed the unconfirmed bash-before-4.4 empty-array claim, the claim about `$@` in older versions and the ShellCheck rule reference.
