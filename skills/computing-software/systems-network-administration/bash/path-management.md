---
id: computing-software.systems-network-administration.bash.path-management
name: path-management
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, path, path-variable, command-lookup, hash, type, which, secure-path, path-order, duplicate-path, shell-environment, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Manage PATH deliberately: the hash cache, type -a, empty PATH elements meaning the current directory, dedup, sudo secure_path, and debugging 'command not found' or wrong version."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Command-Search-and-Execution
  - https://man7.org/linux/man-pages/man5/sudoers.5.html
  - https://specifications.freedesktop.org/basedir-spec/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PATH — command lookup you can reason about

**Goal:** make the right binary win, keep PATH clean across contexts, and explain any
"command not found" or "wrong version" quickly.

## 1. How lookup works
```bash
echo "$PATH" | tr ':' '\n'
type -a python3           # every match: aliases, reserved words, functions, builtins, files
command -v python3        # what will run
hash                      # bash's table of remembered command locations
hash -r                   # forget all remembered locations
```
- PATH is a colon-separated list of directories the shell searches for commands.
- bash remembers the full filename of commands it has found; `hash -r` makes it forget them
  all, and assigning to PATH also clears all hashed filenames. After installing a same-named
  binary earlier in PATH, `hash -r` makes bash search again.
- A zero-length (null) element in PATH (two adjacent colons, or a leading or trailing colon)
  means the current directory. Avoid it, especially for root.
- The default PATH is system-dependent and set by whoever installed bash; check yours with
  `echo "$PATH"` rather than assuming.

## 2. Adding directories
```bash
# in a login-shell startup file such as ~/.profile
[[ -d $HOME/bin ]] && PATH="$HOME/bin:$PATH"
export PATH
```
- Prepend to override system tools, append for fallbacks.
- Guard against growth when a file is sourced repeatedly:
  `case ":$PATH:" in *:/opt/tools/bin:*) ;; *) PATH="/opt/tools/bin:$PATH" ;; esac`

## 3. Deduplicate and inspect
```bash
for d in ${PATH//:/ }; do [[ -d $d ]] || echo "missing: $d"; done
```

## 4. sudo
sudoers(5): if `secure_path` is set, sudo uses that value in place of the user's PATH. So a tool
found in your own PATH may be "command not found" under `sudo`; use its full path or have the
administrator change `secure_path` with `visudo`.

## 5. Debugging recipes
```bash
type -a foo                    # found at all? which one wins?
sudo env | grep ^PATH          # what sudo sees
```

## Failure modes
- "command not found" only under sudo: section 4.
- Wrong version runs after an upgrade: `hash -r`, or another directory earlier in PATH.
- PATH grows each new shell: an unguarded prepend in a file that is sourced repeatedly.

## Verify
- [ ] `command -v tool` resolves to the directory you expect and `hash -r` changes nothing.

## Checked
2026-11-01. Confirmed in the GNU Bash manual: PATH as colon-separated search list, null element
meaning the current directory, system-dependent default, `type -a`, `command`, and the `hash`
builtin including `-r` and clearing on PATH assignment; and in sudoers(5): `secure_path`
replaces the PATH sudo uses. Removed: cron, ssh, systemd and desktop PATH defaults, distro and
merged-usr notes, profile.d recipe and pip/pipx directory notes, none of which the cited pages state.
Method: documentation only; no commands were run.
