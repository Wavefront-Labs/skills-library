---
id: computing-software.devops-ci-cd.semaphore-ui.secrets-directory
name: secrets-directory
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [secrets-path, dirs-secrets, key-store, file-keys, semaphore-ui]
level: advanced
status: docs-checked
description: "Control the one directory Semaphore reads secret files from with dirs.secrets and SEMAPHORE_SECRETS_PATH."
sources:
  - https://semaphoreui.com/docs/admin-guide/configuration/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The secrets directory

Goal: let Key Store file entries and Vault tokens be read from disk safely.

Semaphore reads secret files, such as file-based Key Store entries or HashiCorp Vault and OpenBao tokens read from disk, only from one configurable directory.

| Option | Variable | Meaning |
|---|---|---|
| `dirs.secrets` | `SEMAPHORE_SECRETS_PATH` | Directory for secret files. Default `/tmp/semaphore`. |
| `secrets_path` (legacy) | `SEMAPHORE_SECRETS_PATH` | Top-level setting kept for compatibility; used only when `dirs.secrets` is unset or at the default. |

A non-default `dirs.secrets` wins over the legacy key; setting the environment variable applies to both.

```json
{ "dirs": { "secrets": "/var/lib/semaphore/secrets" } }
```

Key files chosen in the File tab of the Key Store form, and token files referenced by external secret storages, must live inside this directory. Paths outside it are rejected with `file path must be inside secrets path`.

Verify: a file outside the directory is rejected with the error above.

## Checked

2026-11-07. Read in full: the Secrets directory section of the Configuration file page (admin-guide/configuration/config-file.md, whole file read, from the semaphore-docs repository; no snippet files included). Confirmed: the dirs.secrets and legacy secrets_path options, the shared variable, the default /tmp/semaphore, the precedence rules, the example, the File tab and external secret storage token files, and the exact error string. Removed: three gotchas (temp-directory cleanup, read-only mounts, runner location) that the page does not state. The linked Key Store page on env and file sources was not read.
Method: documentation only; no commands were run.
