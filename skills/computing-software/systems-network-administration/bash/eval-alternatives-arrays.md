---
id: computing-software.systems-network-administration.bash.eval-alternatives-arrays
name: eval-alternatives-arrays
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, eval-alternatives-arrays, no-eval, shell-scripting]
level: advanced
status: docs-checked
description: "Replace dangerous eval in bash with arrays, indirect expansion, namerefs and printf %q for dynamic commands and variable names."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eval alternatives
**Goal:** build commands and dynamic names without code injection.
```bash
cmd=(ls -l "$dir"); "${cmd[@]}"            # command as array, not string
name=foo; printf -v "$name" '%s' "$value"   # assign by name
echo "${!name}"                              # indirect read
declare -n ref=foo; ref=new                  # nameref: ref is another name for foo
quoted=$(printf '%q ' "${cmd[@]}")          # string that can be reused as shell input
```
- `eval` joins its arguments with spaces into one command, then reads and runs it, so `eval "$user_input"` executes anything, and `eval "$var=$val"` breaks on `;` or `$()` in val.
- `printf -v var fmt args` assigns the formatted text to `var` instead of printing. `${!name}` reads the variable whose name is in `name` (indirect expansion). A nameref (`declare -n`) makes every reference and assignment act on the variable named by its value.
- `printf %q` writes its argument in a form that can be reused as shell input (ANSI-C quoting when needed, backslash quoting otherwise).
- An array holds a command and its arguments as separate words, so `"${cmd[@]}"` runs them without re-parsing.
- Validate dynamic names before using them: `[[ $name =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]`.
- Self-check: `val='$(touch /tmp/pwn)'` never creates the file.

## Checked
2026-11-08. Confirmed against the Bash Reference Manual: `eval`, `printf -v`, `printf %q`, indirect expansion `${!name}`, the nameref attribute and `[[ =~ ]]`. Removed the `bash 4.3+` label, the ssh example and the claim that untrusted namerefs can be abused, none of which the manual states.
Method: documentation only; no commands were run.
