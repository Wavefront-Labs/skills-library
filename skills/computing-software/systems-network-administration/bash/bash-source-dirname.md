---
id: computing-software.systems-network-administration.bash.bash-source-dirname
name: bash-source-dirname
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, bash-source-dirname, script-dir-bash-source, shell-scripting]
level: practitioner
status: docs-checked
description: "Find the directory of a bash script with BASH_SOURCE, and the cd, CDPATH and pwd -P details that affect the result."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://man7.org/linux/man-pages/man1/readlink.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BASH_SOURCE for the script directory
**Goal:** locate files relative to the script.
```bash
here=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P) || exit 1
source "$here/lib/common.sh"
conf="$here/../etc/app.conf"
```
- `BASH_SOURCE` is a bash array of source filenames: `${FUNCNAME[$i]}` is defined in `${BASH_SOURCE[$i]}` and called from `${BASH_SOURCE[$i+1]}`. Assignments to it have no effect and it cannot be unset. Prefer it to `$0`, which the manual defines as the name of the shell or script, set at shell initialisation (the file name when bash is invoked with a file of commands).
- If the `bash_source_fullpath` shopt option is set, filenames added to `BASH_SOURCE` are converted to full pathnames.
- `pwd -P` prints a path without symbolic links (`pwd -L` may contain them). That resolves symlinks in the directory part only; if the script itself is a symlink, resolve it first with `readlink -f` (GNU readlink canonicalises every symlink in every component; all but the last component must exist).
- When `cd` uses a non-empty `CDPATH` entry it writes the new absolute directory to standard output, which pollutes `$(...)`. Clearing it for the command (`CDPATH= cd ...`) avoids that. A null `CDPATH` entry means the current directory.
- Quote everything and use `--` so odd names are not read as options.
- `BASH_SOURCE` is bash-specific; a plain `sh` script cannot rely on it.
- Self-check: run the script via a symlink and from another directory and compare `$here`.

## Checked
2026-11-09. Confirmed in the bash manual (BASH_SOURCE, `bash_source_fullpath`, `pwd -L/-P`, `cd` and CDPATH behaviour, `$0`) and the readlink man page (`-f`). Removed: the claim that `$0` is the caller's name when a file is sourced, the sourced-versus-executed test line, and the POSIX remark, none of which the cited pages state in those terms.
Method: documentation only; no commands were run.
