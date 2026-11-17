---
id: computing-software.cloud-infrastructure-engineering.docker.gosu-su-exec-privilege-drop-entrypoints
name: gosu-su-exec-privilege-drop-entrypoints
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, entrypoint, gosu, su-exec, signal-forwarding, non-root, pid1, setpriv]
level: advanced
description: "Write an entrypoint that does root-only setup then drops to an app user with exec gosu/su-exec/setpriv so the app becomes PID 1 and receives signals."
sources: ["https://github.com/tianon/gosu", "https://github.com/ncopa/su-exec", "https://github.com/docker-library/postgres/blob/master/docker-entrypoint.sh", "https://docs.docker.com/reference/dockerfile/#entrypoint"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Privilege-dropping entrypoints with gosu / su-exec

**Goal:** start as root to fix volume ownership or bind a setting, then run the app as an
unprivileged user that is PID 1 and gets SIGTERM directly - the pattern used by the official
postgres image entrypoint.

## Entrypoint
```sh
#!/bin/sh
set -e
if [ "$(id -u)" = '0' ]; then
  chown -R app:app /data            # only what must be fixed, not the whole FS
  exec gosu app "$0" "$@"           # re-run this script as app
fi
exec "$@"                            # app replaces the shell -> PID 1
```
```dockerfile
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends gosu; \
    rm -rf /var/lib/apt/lists/*; gosu nobody true
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["app", "serve"]
```
Alpine: `apk add su-exec` and `exec su-exec app "$@"` (use su-exec 0.3 or newer; older
versions had a parser bug).

## Why not su or sudo
`su`/`sudo` have odd TTY and signal-forwarding behaviour (sudo forks rather than execs).
gosu and su-exec switch user, then exec the target directly; they are not a child or
resident process.

## Signal forwarding checklist
- Every `exec` matters: missing it on the last line leaves `sh` as PID 1 swallowing SIGTERM.
- Never run the app in a pipeline (`app | tee log`) in the entrypoint - the pipe keeps sh alive.
- If you must run something after the app (cleanup), you need a real init or a `trap` that
  forwards: `trap 'kill -TERM $pid' TERM; app & pid=$!; wait $pid`.
- Allow `docker run --user 1000` to skip the root branch (the `id -u` test does that).

## Gotchas
- su-exec must be run by root; non-root users cannot change uid/gid.
- `chown -R` on large volumes at every start is slow; check ownership first
  (`[ "$(stat -c %u /data)" != "$(id -u app)" ]`).

## Verify
```sh
docker exec app ps -o pid,user,comm   # PID 1 is the app, user app
time docker stop app                  # fast, no SIGKILL
```

## Checked
2026-10-31. Confirmed from the gosu and su-exec READMEs: exec without staying resident, su/sudo TTY and signal issues, su-exec 0.3 parser bug, su-exec needs root; the postgres entrypoint is a cited source. Removed: redis/mysql claim, PAM remark, setuid warning, setpriv alternative and the capability list (not on pages read).
Method: documentation only; no commands were run.
