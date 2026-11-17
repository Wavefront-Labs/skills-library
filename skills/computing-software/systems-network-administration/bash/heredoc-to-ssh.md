---
id: computing-software.systems-network-administration.bash.heredoc-to-ssh
name: heredoc-to-ssh
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, heredoc-to-ssh, ssh-heredoc, shell-scripting]
level: practitioner
status: docs-checked
description: "Send multi-line scripts to a remote host over ssh with a here document, controlling local versus remote expansion."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://man.openbsd.org/ssh.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Here documents sent to ssh
**Goal:** run several commands remotely in one ssh session.
```bash
ssh "$host" 'bash -s' <<'EOF'            # quoted delimiter: nothing expands locally
  cd /srv/app && git pull
  echo "remote host: $(hostname)"
EOF
ssh -T "$host" bash -s -- "$(printf '%q' "$arg1")" <<'EOF'   # pass values as positional args, quoted for the remote shell
  echo "got $1"
EOF
ssh -T "$host" <<EOF                      # unquoted delimiter: $LOCAL_VAR expands LOCALLY
  echo "$LOCAL_VAR"
EOF
```
- A here document (`<<word`) gives the lines up to the delimiter as standard input to the command. If any part of `word` is quoted, the lines are not expanded; if it is unquoted, they get parameter expansion, command substitution and arithmetic expansion, and `\` must quote `\`, `$` and the backtick. So a quoted delimiter means remote expansion; with an unquoted one escape remote variables as `\$VAR`.
- `<<-word` strips leading tabs, which allows indented here documents inside scripts.
- `bash -s` (or no remaining arguments) makes bash read commands from standard input, and `-s` lets positional parameters be set when reading through a pipe, so extra words after `--` become `$1`, `$2`, ...
- ssh appends the command's arguments to the command, separated by spaces, before sending it to the server, so the remote shell re-parses them. Quote values for the remote side (for example `printf '%q'`) rather than assuming they arrive intact.
- ssh by default requests a pseudo-terminal only for interactive sessions when the client has one; `-T` disables pseudo-terminal allocation. Without a pty the session is transparent and can transfer binary data reliably.
- Self-check: run a here document that only prints `hostname` and confirm it prints the remote name.

## Checked
2026-11-09. Confirmed in the bash manual (here-document quoting and expansion rules, `<<-`, `-s`) and the OpenBSD ssh(1) page (command argument joining, `-T`, pty behaviour). Removed: the claim that passing values as arguments avoids quoting and injection problems (ssh joins arguments with spaces and the remote shell re-parses them), the `set -e` advice, and the original self-check.
Method: documentation only; no commands were run.
