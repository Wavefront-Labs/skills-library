---
id: computing-software.systems-network-administration.bash.rematch-greedy-pitfalls
name: rematch-greedy-pitfalls
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, rematch-greedy-pitfalls, ere-limits, shell-scripting]
level: advanced
status: docs-checked
description: "Avoid bash =~ regex pitfalls: POSIX ERE semantics, quoting of the pattern, BASH_REMATCH scope, and invalid-regex status."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex pitfalls with =~
**Goal:** predictable matching.
```bash
[[ $s =~ ^([0-9]+)-([0-9]+)$ ]] && echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
[[ $s =~ \<([^>]*)\> ]]          # stop at the first > with a negated bracket expression
re='^[[:digit:]]+$'; [[ $x =~ $re ]]   # keep the pattern in a variable, unquoted
```
- The string to the right of `=~` is a POSIX extended regular expression, matched with the POSIX `regcomp` and `regexec` interfaces (see regex(3)). Expect ERE features only; use a bracket expression such as `[[:digit:]]` rather than relying on Perl-style escapes.
- Return value: 0 if the string matches, 1 if not, 2 if the regular expression is syntactically incorrect. With the `nocasematch` shopt option the match ignores case.
- Quote any part of the pattern to match it literally. If the pattern is in a variable, quoting the expansion forces the whole pattern to be literal. Bracket expressions can match special characters without quoting, e.g. `[[ . =~ [.] ]]` matches a literal dot.
- The shell performs word expansion before the regex parser sees the pattern, so shell quoting takes precedence over regex escaping.
- `BASH_REMATCH[0]` is the whole match and `BASH_REMATCH[n]` the nth parenthesised subexpression. Bash sets it in the global scope; declaring it `local` gives unexpected results. Copy values out before running another match.
- For Perl-compatible features use a tool that provides them (for example `grep -P`); bash `=~` does not.
- Self-check: a pattern with an unbalanced parenthesis makes the `[[ ]]` return 2.

## Checked
2026-11-09. Confirmed in the bash manual's section on `[[ ]]` and `=~` (ERE via regcomp/regexec, return values 0/1/2, nocasematch, quoting rules, BASH_REMATCH indices and global scope). Removed: claims about `\d`/`\w` support, lack of lookahead and lazy quantifiers, locale and BSD differences, newline handling, and the printed outputs of the greedy example, which the manual does not state.
Method: documentation only; no commands were run.
