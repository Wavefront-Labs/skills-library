---
id: computing-software.systems-network-administration.bash.set-minus-o-list
name: set-minus-o-list
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, set-minus-o-list, set-o-options, shell-scripting]
level: practitioner
status: docs-checked
description: "List and toggle bash set -o options such as noclobber, pipefail and posix, and print the current option state."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# set -o option list
**Goal:** see and change shell option state.
```bash
set -o                     # print the current option settings
set +o                     # print set commands that recreate them
saved=$(set +o); set -f; ...; eval "$saved"     # restore state
echo "$-"                  # active single-letter flags
set -o pipefail -o noclobber
[[ $- == *e* ]] && echo errexit on
shopt -po errexit          # query via shopt -p -o
```
- Long names and their letters: errexit (-e), nounset (-u), xtrace (-x), noglob (-f), noclobber (-C), functrace (-T), errtrace (-E), monitor (-m); `pipefail`, `posix`, `vi` and `emacs` have no letter.
- `pipefail` makes a pipeline return the rightmost non-zero status (zero if all succeed) and is off by default; `posix` switches Bash to POSIX behaviour where its default differs; `vi` and `emacs` choose the editing interface, which also affects `read -e`.
- `set +o` prints commands that recreate the current settings, so its output can be evaled to restore them around library code.
- The current set of single-letter options is in `$-`. `set` returns zero unless an invalid option is supplied.
- `shopt` toggles the other optional behaviours; `shopt -o` operates on the options `set -o` controls.
- Self-check: `set -o | grep pipefail` shows state; `set -o pipefail` flips it.

## Checked
2026-11-08: confirmed against the GNU Bash Reference Manual (single-page bash.html): The Set Builtin (-o/+o behaviour, option-name list, pipefail, posix, vi/emacs, $-) and The Shopt Builtin (-o, -p). Removed the "himBHs" example flags and the "POSIX-ish" characterisation of set -o. Dropped the POSIX Shell Command Language source, which was not read in this pass.
Method: documentation only; no commands were run.
