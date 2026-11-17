---
id: computing-software.systems-network-administration.bash.env-s-shebang-args
name: env-s-shebang-args
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, env-s-shebang-args, env-split-string, shell-scripting]
level: advanced
status: docs-checked
description: "Pass multiple arguments in a shebang using env -S, and know that most operating systems pass the whole text after the first space as one argument."
sources:
  - https://www.gnu.org/software/coreutils/manual/html_node/env-invocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# env -S for shebang arguments
**Goal:** `#!` lines with flags.
```bash
#!/usr/bin/env -S bash -eu -o pipefail
#!/usr/bin/env -S perl -T -w
```
- Most operating systems (the manual names GNU/Linux and the BSDs) treat all text after the first space on the `#!` line as a single argument. So `#!/usr/bin/env perl -T -w` fails, because the system treats `perl -T -w` as one argument (the program name), with: `/usr/bin/env: 'perl -T -w': No such file or directory`.
- `env -S string` (`--split-string=string`) splits the string into separate arguments. `#!/usr/bin/env -S perl -T -w` is equivalent to running `perl -T -w script` at the prompt.
- Splitting is on unquoted spaces and tabs (newlines, carriage returns, vertical tabs and form feeds count like spaces). Double quotes keep spaces inside one argument, e.g. `#!/usr/bin/env -S awk -v OFS=" xyz " -f`.
- Escapes processed when unquoted or in double quotes: `\c \f \n \r \t \v \# \$ \_ \" \' \\`. Single quotes disable them except `\'` and `\\`. `\_` is an argument separator outside quotes and a space inside double quotes.
- A `#` starting an argument ignores the rest of the string; `\#` gives a literal `#`.
- `${VARNAME}` (braces required) is expanded by env, not by a shell; `$VARNAME` without braces makes env fail with `only ${VARNAME} expansion is supported`.
- To test on the command line quote the string: `env -S'perl -T -w' hello.pl`. In a shebang line the quotes are not needed. For troubleshooting put `-v` first: `#!/usr/bin/env -vS perl -T -w`.
- `env -S` is listed in the coreutils manual as supporting FreeBSD's syntax; how old a given `env` is, and what other systems provide, is not stated there.

## Checked
Date: 2026-11-07
Method: Read GNU coreutils manual section 23.2 env in full, including 23.2.2 `-S` usage in scripts and 23.2.3 `-S` syntax (whitespace splitting, escapes, comments, variable expansion). Corrections: the draft's error text "No such file: bash -e" replaced with the manual's actual message; "On Linux" widened to the manual's "most operating systems (GNU/Linux, BSDs)". Removed the "coreutils 8.30+, FreeBSD, macOS" and "unavailable in old coreutils/busybox" version claims, the `set -euo pipefail` alternative and portable-shebang advice, and the `bash -x ./script.sh` self-check, none of which the page states.
