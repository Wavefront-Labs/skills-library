---
id: computing-software.systems-network-administration.bash.shell-quoting-and-word-splitting
name: shell-quoting-and-word-splitting
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-quoting, word-splitting, ifs, double-quotes]
level: practitioner
status: docs-checked
description: "Quote expansions correctly to prevent word splitting and globbing, and know when quotes are optional."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quoting and word splitting

- The shell splits the results of parameter expansion, command substitution and arithmetic expansion that did not occur within double quotes into words; words that were not expanded are not split. If `IFS` is unset, splitting behaves as if it were space, tab, newline; if `IFS` is null, no splitting happens. A filename with a space becomes two arguments when the expansion is unquoted. Rule: quote every expansion: `"$var"`, `"$(cmd)"`, `"${arr[@]}"`.
- A plain assignment value (`x=$y`) is a context where word splitting is not performed (the manual gives the value of an assignment as an example).
- On the right of `==` and `!=` inside `[[ ]]` the text is a pattern; quote it to match literally.
- Single quotes preserve every character literally, and a single quote cannot appear between single quotes, even after a backslash. To include one, close the quotes and escape it outside them: `'it'\''s'`.
- Double quotes preserve all characters except `$`, backtick, `\` and, with history expansion on, `!`. The backslash keeps its meaning only before `$`, backtick, `"`, `\` or newline.
- A non-quoted backslash preserves the literal value of the next character (a backslash-newline pair is a line continuation).
- `$'...'` is a Bash form of single quotes with ANSI C backslash escapes decoded.
- `"$@"` expands each positional parameter to a separate word, like `"$1" "$2" ...`, and expands to nothing when there are none. `"$*"` is one word with parameters joined by the first character of IFS. Unquoted `$@` and `$*` are subject to further splitting and filename expansion.
- Pass lists via arrays, not strings: `args=(--flag "$file"); cmd "${args[@]}"`; `"${name[@]}"` expands to separate words like `"$@"`.
- Verify: `touch "a b"; for f in $(ls); do echo "[$f]"; done` shows the splitting bug (`$(ls)` output is split); `for f in *; do echo "[$f]"; done` does not.

## Checked
Checked 2026-11-08 against the Bash Reference Manual: Quoting (escape character, single, double, ANSI-C), Special Parameters (`*`, `@`), Word Splitting, Conditional Constructs (`[[ ==`). Removed claims the manual does not state or that I could not locate: that `case $x in` and here-strings need no quotes, that `[[ ]]` does no splitting, the `rm -- "$file"` advice and the ShellCheck SC2086 pointer. Replaced the `https://www.gnu.org/software/bash/manual/` and POSIX landing-page sources with the single-page manual.

Method: docs-only read of cited pages, 2026-11-08
