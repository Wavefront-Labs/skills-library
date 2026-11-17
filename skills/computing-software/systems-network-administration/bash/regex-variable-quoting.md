---
id: computing-software.systems-network-administration.bash.regex-variable-quoting
name: regex-variable-quoting
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, regex-variable-quoting, rematch-quoting, shell-scripting]
level: advanced
status: docs-checked
description: "Store regex patterns in bash variables for [[ =~ ]] and leave them unquoted so special characters stay regex, not literal."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regex in a variable
**Goal:** reusable patterns whose quoting is predictable.
```bash
re='^[0-9]{3}-[0-9]{4}$'
[[ $phone =~ $re ]] && echo ok           # unquoted variable: regex
[[ $phone =~ "$re" ]]                     # QUOTED: whole pattern matched literally
[[ $x =~ ^"$prefix"[0-9]+$ ]]            # quote ONLY the part that must be literal
```
- The right side of `=~` is a POSIX extended regular expression; quote any part of it to match that part literally. Quoting the variable expansion forces the entire pattern to be literal.
- You cannot quote `^` or `$` and still anchor: `[[ $line =~ ^"initial string" ]]` works, `[[ $line =~ "^initial string" ]]` does not.
- Storing the pattern in a variable avoids shell-quoting problems with characters special to the shell, and with backslashes: `pattern='\.'` then `[[ . =~ $pattern ]]` matches, but `[[ . =~ "$pattern" ]]` does not.
- A bracket expression such as `[.]` matches a special character without quoting.
- `shopt -s compat31` (bash-3.1 compatibility) makes quoting the right side of `=~` have no special effect; the manual calls compatibility levels a temporary solution, so do not rely on it.
- Case-insensitive: `shopt -s nocasematch`.
- The match succeeds if the pattern matches any part of the string; anchor with `^` and `$` for a whole-string match. A syntactically wrong regex returns 2.
- Self-check: the unquoted form matches; the quoted form does not.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Conditional Constructs, Shell Compatibility Mode, Shopt Builtin). Confirmed quoting rules, the `^"..."` example, the `pattern='\.'` example, `nocasematch`, compat31 and return status 2. Removed the claim that the quoting change happened in bash 3.2 and the line about spaces inside variables, which were not confirmed.
