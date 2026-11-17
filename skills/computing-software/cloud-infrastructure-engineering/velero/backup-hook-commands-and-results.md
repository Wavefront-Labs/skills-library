---
id: computing-software.cloud-infrastructure-engineering.velero.backup-hook-commands-and-results
name: backup-hook-commands-and-results
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [hook-command, shell-hooks, hooksattempted, hooksfailed, backup-describe]
level: practitioner
status: docs-checked
description: "Write multi-command and env-var backup hooks by wrapping them in a shell, and read HooksAttempted and HooksFailed from backup describe."
sources:
  - https://velero.io/docs/main/backup-hooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hook commands run without a shell. If you need a shell feature, put the shell first in the command. The container must have that shell.

Multiple commands: wrap them in a shell and chain with `;` or `&&`.

```shell
pre.hook.backup.velero.io/command='["/bin/bash", "-c", "echo hello > hello.txt && echo goodbye > goodbye.txt"]'
```

Environment variables from the pod are only available when a shell runs the command. Example, using `MYSQL_ROOT_PASSWORD` defined in the mysql pod:

```yaml
pre:
- exec:
    container: mysql
    command:
      - /bin/sh
      - -c
      - mysql --password=$MYSQL_ROOT_PASSWORD -e "FLUSH TABLES WITH READ LOCK"
    onError: Fail
```

Results are recorded and shown by:

```bash
velero backup describe <backup name>
```

The output includes `HooksAttempted` and `HooksFailed` counts, for example `HooksAttempted: 1` and `HooksFailed: 0`. Detailed failure reasons appear in the `Errors` section.

`onError` defaults to `Fail` and accepts `Fail` or `Continue`. The hook timeout defaults to 30s.

## Checked

2026-11-08. Read in full: the Backup Hooks page. Every remaining claim was confirmed there. Removed or reworded: the claim about how a failing hook marks the backup item and the table-lock advice.

Method: documentation only; no commands were run.
