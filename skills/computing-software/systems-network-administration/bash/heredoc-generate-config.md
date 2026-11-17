---
id: computing-software.systems-network-administration.bash.heredoc-generate-config
name: heredoc-generate-config
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, heredoc-generate-config, heredoc-template, shell-scripting]
level: practitioner
status: docs-checked
description: "Write config files from bash with cat and here documents, controlling variable expansion and tab-indented bodies."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating config files with heredocs
**Goal:** create files from templates in scripts.
```bash
cat > "$conf" <<EOF
listen_port = ${PORT:-8080}
user = $(id -un)
EOF
cat <<'EOF' | sudo tee /etc/app/app.conf >/dev/null    # root-owned target
path = $HOME/data      # stays literal
EOF
cat >> "$f" <<-EOF
	indented with tabs, stripped by <<-
	EOF
```
- With an unquoted delimiter the body is treated like a double-quoted string: parameter expansion, command substitution and arithmetic expansion happen, and `\` must be used to quote `\`, `$` and a backtick; double quotes have no special meaning. If any part of the delimiter word is quoted (`'EOF'`), the body is not expanded.
- The delimiter word itself is not expanded, and the closing delimiter must be alone on its line with no trailing blanks.
- `<<-` strips leading tab characters (not spaces) from the body lines and from the delimiter line, so heredocs can be indented in scripts.
- With an unquoted delimiter, backslash-newline joins lines before the end-delimiter check.
- Self-check: `cat <<'E'` containing `$HOME` prints the literal text.

## Checked
2026-11-08. Confirmed against the Bash Reference Manual, section Here Documents: quoted versus unquoted delimiter, which expansions run, `<<-` tab stripping, delimiter rules and backslash-newline. Removed the claims about `sudo cat >` versus `sudo tee` and the `install -m 600` permission trick, because the manual does not cover them.
Method: documentation only; no commands were run.
