---
id: computing-software.systems-network-administration.bash.umask-077-subshell
name: umask-077-subshell
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, umask-077-subshell, umask-subshell, shell-scripting]
level: practitioner
status: docs-checked
description: "Create files with restrictive modes in shell by scoping umask 077 in a subshell, restoring a saved umask and reading umask -S output."
sources:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/umask.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scoped umask 077
**Goal:** private files without changing the rest of the script.
```bash
( umask 077; : > "$keyfile" )                 # the umask change stays in the subshell
umask -S                                      # symbolic form, e.g. u=rwx,g=rwx,o=rx
old=$(umask); umask 027; : > "$other"; umask "$old"
```
- `umask mask` sets the file mode creation mask of the current shell execution environment; it affects the initial permission bits of files created afterwards, including files created by redirections in that environment.
- Calling `umask` in a subshell or a separate utility execution environment does not affect the caller's mask: `(umask 002)`, `nohup umask ...` and `find . -exec umask ... \;` all leave it unchanged. So `( umask 077; cmd > out )` restricts only that subshell.
- With no operand, `umask` writes the current mask to standard output. The default output format is unspecified, but a later `umask` on the same system accepts it as a mask operand, which is what makes `old=$(umask); ...; umask "$old"` safe.
- `umask -S` prints `u=%s,g=%s,o=%s` where each letter present means the bit is clear in the mask (the permission is allowed). The octal form sets the given bits in the mask; the symbolic form of the operand names permissions that are left alone, so `umask a=rx,ug+w` and `umask 002` both clear only the other-write bit.
- In a symbolic operand, `+` clears the named bits in the mask and `-` sets them, relative to the current mask.
- The exit status is 0 if the mask was changed or no operand was given, greater than 0 on error. The standard says umask is generally provided as a shell regular built-in because it affects the current shell environment.

## Checked
Date: 2026-11-07
Method: Read the POSIX umask utility page in full (description, operands, -S format, examples, exit status) and the subshell paragraph of the Shell Command Language execution-environment section. Trims: removed the "666/777 minus umask" arithmetic table, the claim that umask cannot add execute bits, the chmod race-window statement, the `openssl genrsa` and `install -m 600 /dev/null` lines and the `stat -c %a` self-check, because none appear on these pages. The description was reworded to match.
