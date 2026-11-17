---
id: computing-software.systems-network-administration.bash.getopt-gnu-long-options
name: getopt-gnu-long-options
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, getopt-gnu-long-options, getopt-long, shell-scripting]
level: advanced
status: docs-checked
description: "Parse long options such as --output=file with the enhanced util-linux getopt in bash, with the quoting and test rules."
sources:
  - https://man7.org/linux/man-pages/man1/getopt.1.html
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GNU getopt for long options
**Goal:** support `--long` and `-s` forms together.
```bash
opts=$(getopt -o vo:h -l verbose,output:,help -n "$0" -- "$@") || exit 2
eval set -- "$opts"
while true; do
  case $1 in
    -v|--verbose) verbose=1; shift ;;
    -o|--output)  out=$2; shift 2 ;;
    -h|--help)    usage; exit 0 ;;
    --) shift; break ;;
  esac
done
echo "operands: $*"
```
- The enhanced getopt(1) (util-linux) outputs quoted arguments that preserve whitespace and special characters; the shell must interpret that output again, usually with `eval`, hence `eval set -- "$opts"`. Call it in the form `getopt -o shortopts -l longopts -- "$@"` (the second or third SYNOPSIS format) rather than the traditional compatible form.
- Detect the enhanced version with `getopt -T`: it prints nothing and sets exit status 4. Other implementations, and this one when `GETOPT_COMPATIBLE` is set, return `--` and status 0.
- `-o` gives short options and `-l` long ones (comma-separated, option may be repeated). One colon after a name means a required argument, two colons an optional argument.
- An optional argument must be written directly after the short option character, or after the long option name separated by `=`.
- A required long-option argument may follow `=` or be the next parameter. Long options may be abbreviated if not ambiguous.
- Every parameter after `--` is a non-option parameter. If `POSIXLY_CORRECT` is set, or the short option string starts with `+`, parsing stops at the first non-option parameter.
- `-n` sets the program name used when getopt(3) reports errors. On a parsing problem getopt writes to stderr and returns a nonzero status, so test it as above.
- No getopt? Loop with `case` on `--output=*` and strip with `${1#*=}` (`${parameter#word}` removes the shortest leading match).
- Self-check: `./script --output=x -v a` gives `out=x`, `verbose=1`, operand `a`.

## Checked
2026-11-09. Confirmed in the getopt(1) man page (util-linux): quoted output and `eval`, `-T` and status 4, `GETOPT_COMPATIBLE`, `-o`/`-l`/`-n`, colon syntax, optional-argument rule, `--`, `+`, `POSIXLY_CORRECT`, error status; and the bash manual for `${parameter#word}`. Removed: the claim about macOS/BSD getopt lacking long options and the `exit 2` rationale beyond "nonzero on error".
Method: documentation only; no commands were run.
