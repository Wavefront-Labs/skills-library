---
id: computing-software.systems-network-administration.bash.dash-local-keyword
name: dash-local-keyword
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, dash-local-keyword, sh-local, shell-scripting]
level: advanced
status: docs-checked
description: "Use local in POSIX sh scripts safely: POSIX does not specify it, so check the target shell or use a function body in parentheses for scope."
sources:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local in POSIX sh
**Goal:** keep function variables from leaking in /bin/sh scripts.
```sh
f() {
  local x=1 y            # bash builtin; not specified by POSIX
  y=$(( x + 1 ))
  echo "$y"
}
g() ( x=1; echo "$x" )   # parentheses: the function body runs in a subshell
```
- Bash: `local [option] name[=value] ...` creates a local variable, usable only within a function, with scope limited to that function and its children (functions it calls); using it outside a function is an error. Options are those accepted by `declare`. `local -` makes `set` option changes inside the function restore on return.
- POSIX does not specify `local`: it is in the table of names for which, when it is a command name, "the results are unspecified" (section 2.9.1.4 Command Search and Execution). Check the target `/bin/sh` before relying on it.
- POSIX function definitions take a compound command, `fname ( ) compound-command`, so a subshell body `f() ( ... )` is valid. Commands grouped with parentheses run in a subshell environment, and changes made there "shall not affect the shell environment". Variables set in the body therefore cannot leak, but the body also cannot set variables for the caller; return values go through standard output or the exit status.
- POSIX positional parameters are restored when a function completes; plain variables are not.
- Where `local` is unavailable, a naming prefix (such as `_f_x`) limits collisions but does not scope the variable.
- The function name must be a valid name and not the name of a special built-in utility; functions and variables have separate name spaces.

## Checked
Date: 2026-11-07
Method: Read POSIX Shell Command Language sections 2.9.1.4 Command Search and Execution (the unspecified-names table containing `local`), 2.9.5 Function Definition Command, and the subshell paragraph in the Shell Execution Environment section; read the GNU Bash manual local builtin entry and the shell-function variable-scope paragraphs. Trims: removed the claims that dash and busybox ash implement `local`, that `local -r`, `local -a` and `local x=$(cmd)` status differ between shells, that `local x` leaves x unset in dash and bash, and the `checkbashisms` self-check, none of which the sources confirm.
