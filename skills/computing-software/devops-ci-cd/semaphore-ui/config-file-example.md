---
id: computing-software.devops-ci-cd.semaphore-ui.config-file-example
name: config-file-example
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [config-json, configuration, cookie-hash, access-key-encryption, semaphore-ui]
level: practitioner
status: docs-checked
description: "Read and write config.json: database block, secrets, remote runner flags, schedule timezone, logging and tmp path."
sources:
  - https://semaphoreui.com/docs/admin-guide/configuration/config-file
  - https://semaphoreui.com/docs/reference/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The config.json file

Goal: understand the main keys of Semaphore's configuration file.

Typical content:

```json
{
  "mysql": { "host": "127.0.0.1:3306", "user": "root", "pass": "***", "name": "semaphore" },
  "dialect": "mysql",
  "git_client": "go_git",
  "git_attempts": 4,
  "mfa": { "totp": { "enabled": false, "allow_recovery": true } },
  "tmp_path": "/tmp/semaphore",
  "cookie_hash": "96Nt***",
  "cookie_encryption": "x0bs***",
  "access_key_encryption": "j1ia***",
  "max_tasks_per_template": 3,
  "schedule": { "timezone": "UTC" },
  "process": { "chroot": "/opt/semaphore/sandbox" }
}
```

Meaning of notable keys: `dialect` picks the database block (`mysql`, `postgres`, `sqlite`); `tmp_path` (default `/tmp/semaphore`) is where Semaphore stores ephemeral projects; `max_tasks_per_template` is the number of recent tasks kept in the database per template (not a concurrency limit; `max_parallel_tasks` is the concurrency setting); `process.chroot` is the chroot directory for wrapped processes; `log.events` configures event logging (Pro).

`use_remote_runner` and `runner_registration_token` are deprecated in the configuration reference; use the Runners field instead. Two official pages disagree with each other here: the config-file page's own example labels the MySQL block `mysql_test` and the TOTP block `auth.totp`, while the configuration reference and the local accounts page use `mysql` (with `postgres` and `sqlite` alongside) and `mfa.totp`. This skill follows the reference.

Use the file with `semaphore server --config ./config.json` or `semaphore runner start --config ./config.json`.

Gotchas:
- JSON has no comments or trailing commas.
- Changing `cookie_encryption` signs every user out; back up the encryption keys separately from the database, which is unreadable without them.

Verify: the server starts without a config parse error in stdout.

## Checked

2026-11-04: checked against the config file page and the configuration reference. Removed deprecated runner options from the sample, corrected the meaning of tmp_path, max_tasks_per_template, chroot and log.events, and removed an unconfirmed restart gotcha. The two pages disagree (mysql_test and auth.totp versus mysql and mfa.totp); the skill says so and follows the reference.

Method: documentation only; no commands were run.
