---
id: computing-software.systems-network-administration.bash.source-relative-path
name: source-relative-path
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, source-relative-path, source-relative, shell-scripting]
level: practitioner
status: docs-checked
description: "Source library files relative to the script, not the current directory, and handle missing files."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sourcing relative to the script
**Goal:** `source` that works from any cwd.
```bash
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source "$here/lib/common.sh" || { echo "cannot load common.sh" >&2; exit 1; }
[ -r "$f" ] && . "$f"                    # dot command, same as source
source lib/common.sh arg1                # args become the library's $1 while it runs
```
- `source` and `.` are equivalent: they read and execute the file in the current shell. If the filename has no slash, bash searches the directories in `PATH` (or `-p path` if given); when not in POSIX mode it then also searches the current directory. So a bare `source lib.sh` depends on `PATH` and cwd; use an explicit path built from `BASH_SOURCE` instead.
- With arguments, they become the positional parameters while the file runs; otherwise the positionals are unchanged.
- The return status is that of the last command executed in the file, or zero if none; it is non-zero if the file is not found or cannot be read, hence the `||` guard above.
- `BASH_SOURCE` holds the source filenames; `${BASH_SOURCE[0]}` is the file the function or code is defined in.
- Self-check: run the script from `/` and from its own directory.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Bourne Shell Builtins `.`, Bash Variables BASH_SOURCE). Confirmed the search order, argument and return-status behaviour. Removed the claims about cron, POSIX-mode abort on a missing file, ShellCheck source hints and `return` at top level of a sourced file, which were not confirmed in the pages read.
