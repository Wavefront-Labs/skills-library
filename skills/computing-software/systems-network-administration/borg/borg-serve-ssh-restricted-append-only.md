---
id: computing-software.systems-network-administration.borg.borg-serve-ssh-restricted-append-only
name: borg-serve-ssh-restricted-append-only
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-serve, ssh, authorized-keys, restrict-to-path, append-only, storage-quota, forced-command]
level: advanced
status: docs-checked
description: "Lock down Borg SSH backup clients with borg serve forced commands in authorized_keys: restrict-to-path, restrict-to-repository, append-only, quota and keepalives."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/serve.html", "https://borgbackup.readthedocs.io/en/stable/usage/init.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg serve over SSH

`borg serve` is the server side of a remote repository and is normally started by SSH, not by hand. Pin each client key to a forced command in the server's `authorized_keys`:

```
command="borg serve --restrict-to-path /path/to/repo",restrict ssh-ed25519 AAAA...
command="borg serve --restrict-to-repository /path/to/repo --append-only",restrict ssh-ed25519 AAAA...
```

- `--restrict-to-path PATH`: access to PATH and subdirectories (repeatable; PATH need not be a repository).
- `--restrict-to-repository PATH`: only that exact repository; the directory may be empty or missing so a client can run `init`.
- `--append-only`: only append to segment files. This is low-level only: delete, prune and reading are still allowed by the protocol.
- `--storage-quota`: server-side quota that overrides the repository's own.

Notes: use `restrict` (OpenSSH 7.2+; older versions need explicit `no-*` options). When `SSH_ORIGINAL_COMMAND` is set, only log-level, debug and `--lock-wait` are taken from it; client `BORG_XXX` variables are ignored, so set server variables inside the forced command (`command="BORG_XXX=value borg serve ..."`). Send SSH keepalives from both ends every 10 seconds with count 30, and use `--lock-wait 600`, so stale serve processes exit and release locks. Give the backup user a minimal login shell.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/serve and usage/init): serve options, SSH_ORIGINAL_COMMAND allowlist, restrict versus no-* options, keepalive and lock-wait values, minimal shell. Removed: the server-side transaction-log review suggestion (not in the page).

Method: documentation only; no commands were run.
