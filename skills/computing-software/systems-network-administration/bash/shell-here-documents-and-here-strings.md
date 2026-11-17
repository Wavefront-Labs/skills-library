---
id: computing-software.systems-network-administration.bash.shell-here-documents-and-here-strings
name: shell-here-documents-and-here-strings
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-heredoc, here-string, heredoc-quoting, indent-heredoc]
level: practitioner
status: docs-checked
description: "Write here-documents with correct quoting and indentation and use here-strings for input."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Here-documents

- `cmd <<EOF ... EOF` feeds the lines read up to the delimiter to stdin; the delimiter must be alone on its line with no trailing blanks. Unquoted delimiter: the text is treated like a double-quoted string, so parameter expansion, command substitution and arithmetic expansion happen and `\` must quote `\`, `$` and a backtick. Quoting any part of the delimiter (`<<'EOF'`) means the lines are not expanded, which is what you want for generating scripts, YAML and SQL containing `$`.
- `<<-EOF` strips leading TAB characters from input lines and from the delimiter line, letting you indent bodies inside scripts. Spaces are not stripped, so editors that convert tabs to spaces break it.
- Here-string: `grep foo <<< "$text"` supplies the expanded word, with a newline appended, on stdin. Word splitting and filename expansion are not performed on it.
- Write files with `cat > "$f" <<'EOF'`.
- Redirections attach to the command that reads them: `ssh host bash -s <<'EOF'`. Quote the delimiter so the local shell does not expand variables meant for the remote side.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual, Here Documents and Here Strings. Confirmed delimiter rules, quoted versus unquoted expansion, `<<-` tab stripping and here-string expansion and newline. Removed the zsh and POSIX-alternative claims, the `sudo tee` advice, the claim that large here-documents use temp files or pipes, and the landing-page sources.
