---
id: computing-software.systems-network-administration.bash.grep-q-before-append
name: grep-q-before-append
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, grep-q-before-append, append-if-missing, shell-scripting]
level: practitioner
status: draft
description: "Append a line or block to a config file only if missing, with grep -qxF, marker blocks and sed replace for edits."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Append a line only if absent
**Goal:** idempotent edits to text files.
```bash
line='export EDITOR=vim'
grep -qxF -- "$line" ~/.profile || printf '%s\n' "$line" >> ~/.profile
# marker block: replace in place on re-run
sed -i '/# BEGIN app/,/# END app/d' "$f"
printf '# BEGIN app\n%s\n# END app\n' "$block" >> "$f"
# change a setting if present, add if not
grep -q '^PermitRootLogin' "$f" && sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' "$f" || echo 'PermitRootLogin no' >> "$f"
```
- `-F` fixed string, `-x` whole line, `-q` quiet: no regex surprises.
- `sed -i` differs on macOS (`-i ''`); and keep a backup `-i.bak` for risky edits.
- File may lack a trailing newline: guard with `tail -c1 "$f" | read -r _ || echo >> "$f"`.
- Validate the result (e.g. `sshd -t`) before reloading.
- Self-check: run twice, `grep -c` finds exactly one line.
