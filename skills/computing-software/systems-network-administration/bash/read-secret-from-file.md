---
id: computing-software.systems-network-administration.bash.read-secret-from-file
name: read-secret-from-file
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, read-secret-from-file, secrets-from-file, shell-scripting]
level: practitioner
status: draft
description: "Pass secrets to commands from files, env files or stdin instead of arguments, with mode checks, in shell scripts."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading secrets from files
**Goal:** keep secrets out of `ps`, history and logs.
```bash
secret_file=/etc/app/secret
[ "$(stat -c %a "$secret_file")" = 600 ] || { echo "bad mode" >&2; exit 1; }
pw=$(<"$secret_file")                       # no cat, no trailing newline issue beyond $( )
mysql --defaults-extra-file=/etc/app/my.cnf # config file holding credentials
curl -H @- https://api <<<"Authorization: Bearer $pw"   # header via stdin (curl 7.55+)
docker login -u user --password-stdin < "$secret_file"
set +x                                       # never trace around secrets
```
- Environment variables are visible in `/proc/PID/environ` to the same user/root and inherited by children.
- Command-line arguments are world-readable via `ps`.
- Files: mode 600, owned by the service user, outside repos; `umask 077` before creating.
- Use systemd `LoadCredential=` or a secrets manager where available.
- Self-check: `ps aux | grep secret` shows nothing sensitive.
