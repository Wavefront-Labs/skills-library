---
id: computing-software.systems-network-administration.borg.borg-env-vars-and-return-codes
name: borg-env-vars-and-return-codes
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, environment-variables, borg-passphrase, borg-passcommand, borg-repo, borg-rsh, exit-codes, repository-url, automation]
level: practitioner
status: docs-checked
description: "Script Borg unattended: BORG_REPO, BORG_PASSPHRASE, BORG_PASSCOMMAND, BORG_RSH and directory variables, repository URL forms, and return codes 0, 1, 2."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/general.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg environment variables, URLs and return codes

Key variables:

- `BORG_REPO`: default repository; `::archive` abbreviates an archive path.
- `BORG_PASSPHRASE` > `BORG_PASSCOMMAND` > `BORG_PASSPHRASE_FD` (in that precedence). PASSCOMMAND runs without a shell (`$HOME` expands, `~` does not). PASSPHRASE_FD is called safer, since other processes may read the environment.
- `BORG_NEW_PASSPHRASE`: answers the new-passphrase prompt (for `key change-passphrase`).
- `BORG_RSH`: replace ssh, e.g. `ssh -i /path/to/key`. `BORG_REMOTE_PATH`: remote borg binary name.
- `BORG_CACHE_DIR`, `BORG_CONFIG_DIR`, `BORG_KEYS_DIR` (default `$BORG_CONFIG_DIR/keys`), `BORG_SECURITY_DIR` (nonce and state tracking).
- Prompt answers: `BORG_RELOCATED_REPO_ACCESS_IS_OK`, `BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK` (yes/no), `BORG_CHECK_I_KNOW_WHAT_I_AM_DOING` and `BORG_DELETE_I_KNOW_WHAT_I_AM_DOING` (case-sensitive YES/NO).
- Lock wait is the `--lock-wait SECONDS` option (default 1).

Repository URLs: local path or `file://`; `ssh://user@host:port/path/to/repo` (`/./` relative to cwd, `/~/` relative to home); deprecated SCP style `user@host:path`.

Return codes: 0 success; 1 warning (finished, check the log, for example unreadable files); 2 error; 128+N killed by signal N. With `BORG_EXIT_CODES=modern`, 3-99 are specific errors and 100-127 specific warnings.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/general): environment variables, precedence, repository URL forms, return codes and BORG_EXIT_CODES=modern. Removed: the closing scripting tip (not in the page).

Method: documentation only; no commands were run.
