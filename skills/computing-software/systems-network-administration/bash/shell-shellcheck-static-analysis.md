---
id: computing-software.systems-network-administration.bash.shell-shellcheck-static-analysis
name: shell-shellcheck-static-analysis
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-shellcheck, shell-linting, sc-codes]
level: practitioner
status: docs-checked
description: "Lint shell scripts with ShellCheck: the common SC codes, their wiki pages, and what static analysis does not cover."
sources:
  - https://www.shellcheck.net/wiki/
  - https://www.shellcheck.net/wiki/SC2002
  - https://www.shellcheck.net/wiki/SC2086
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ShellCheck

- `shellcheck script.sh` reports problems with SC codes. Every code has a wiki page at `https://www.shellcheck.net/wiki/SCnnnn` explaining the problem and the fix. Common ones from the wiki index:
  - SC2086: double quote to prevent globbing and word splitting.
  - SC2046: quote `$(...)` to prevent word splitting.
  - SC2155: declare and assign separately to avoid masking return values.
  - SC2164: use `cd ... || exit` in case `cd` fails.
  - SC2012: use `find` instead of `ls` to better handle non-alphanumeric filenames.
  - SC2034: a variable appears unused; verify it or export it.
  - SC2002: useless cat. An optional rule: since ShellCheck 0.11.0 it must be enabled with `enable=useless-use-of-cat` in `.shellcheckrc` (the long name replaces the SC code for optional rules).
- Warnings can be ignored case by case when you have a reason; keep exceptions narrow and explain them in a comment rather than disabling a check for a whole codebase.
- ShellCheck is a static analysis tool: it does not run the script. Pair it with tests, and with `bash -n` (read commands without executing them), which only checks syntax.
- Fix the root cause the wiki describes (for example an array instead of a split string for SC2086) before reaching for an ignore.

## Checked
2026-11-09. Confirmed in the ShellCheck wiki index and the SC2002 and SC2086 pages (code titles, optional-rule note, "static analysis tool" wording), and the bash manual (`-n` syntax check). Removed: severity and format flags (`-S`, `-f`), `-s` / `-x` / `source=` directives, the `disable=` comment syntax, shfmt usage, editor integration and exit-status claims, none of which appear on the pages read.
Method: documentation only; no commands were run.
