---
id: computing-software.database-administration.pgbackrest.lock-path-and-allow-root
name: lock-path-and-allow-root
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, lock-path, allow-root, permissions, neutral-umask]
level: advanced
status: docs-checked
description: "Lock files, running as root, and the neutral umask that sets repository file modes."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid permission problems and concurrent-run conflicts.

- `lock-path` (default /tmp/pgbackrest) holds lock files that prevent conflicting operations running concurrently.
- `allow-root` (default n): only `restore` may run as root by default, because it manages file ownership carefully. Other commands as root risk creating root-owned files, for example in the repository, which the PostgreSQL user cannot access and later commands fail. The docs say it is far better to run pgBackRest as the user that owns the repository and cluster.
- `neutral-umask` (default y): sets the umask to 0000 so repository modes come out sensible: directories 0750, files 0640. Use `neutral-umask=n` or `--no-neutral-umask` to use the executing user's umask.
- `priority` sets process priority (-20 to 19).

```
[global]
lock-path=/path/to/locks
neutral-umask=y
```

On a dedicated repository host, create a separate repository user such as pgbackrest rather than using postgres. If PostgreSQL runs on the repository host, put postgres in the pgbackrest group so it can read but not damage the repository.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Nothing needed removing. 

Method: documentation only; no commands were run.
