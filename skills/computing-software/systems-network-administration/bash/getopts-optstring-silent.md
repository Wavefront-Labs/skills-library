---
id: computing-software.systems-network-administration.bash.getopts-optstring-silent
name: getopts-optstring-silent
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, getopts-optstring-silent, optind-optarg, shell-scripting]
level: practitioner
status: docs-checked
description: "Parse short options with getopts, using a leading colon for silent errors, OPTARG, OPTIND and shift."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/getopts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# getopts silent mode and OPTIND
**Goal:** robust short-option parsing.
```bash
usage() { echo "usage: $0 [-v] [-o file] args" >&2; exit 2; }
verbose=0
while getopts ':vo:h' opt; do
  case $opt in
    v) verbose=1 ;;
    o) out=$OPTARG ;;
    h) usage ;;
    :) echo "-$OPTARG needs a value" >&2; usage ;;
    \?) echo "bad option -$OPTARG" >&2; usage ;;
  esac
done
shift $((OPTIND - 1))        # remaining positional args
```
- `getopts optstring name [arg ...]`: a character followed by a colon takes an argument, which is placed in `OPTARG`. `:` and `?` cannot be used as option characters.
- If the first character of optstring is a colon, getopts is silent. An unknown option sets `name` to `?` and `OPTARG` to the option character, with no diagnostic. A missing argument sets `name` to `:` and `OPTARG` to the option character. Without the leading colon, both cases set `name` to `?`, unset `OPTARG` and print a diagnostic (setting `OPTERR=0` in bash also suppresses it).
- getopts returns true if an option is found, specified or not, and false at the end of options or on error. At the end of options `OPTIND` is the index of the first non-option argument and `name` is `?`.
- The end of options is the first `--` that is not an option-argument, or the first element that does not begin with `-`, or an error. So options must come before operands, and getopts parses only single-character options.
- `OPTIND` starts at 1 each time the shell or script is invoked and is not reset automatically; set `OPTIND=1` before parsing a new set of parameters in the same shell (for example in a function called more than once).
- By default it parses the positional parameters; extra `arg` operands are parsed instead if supplied.
- `getopts` is a POSIX utility, so this pattern is specified by both the Bash manual and POSIX.

## Checked
Date: 2026-11-07
Method: Read the GNU Bash manual getopts entry and the POSIX getopts utility page in full. Trims: removed "works in dash" (neither page mentions it), the invented `./script -x` self-check, and changed the `--` and "no long options" lines to the POSIX wording on how the end of options is determined. Added the exact OPTARG/name values for silent and non-silent modes from both pages. The POSIX V3_chap02 source was dropped from sources because only the getopts page was used.
