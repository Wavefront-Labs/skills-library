---
id: computing-software.devops-ci-cd.forgejo.ssh-authorized-keys-command
name: ssh-authorized-keys-command
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [authorizedkeyscommand, authorized-keys, forgejo-keys, ssh-scaling]
level: advanced
status: docs-checked
description: "Serve SSH keys on demand with AuthorizedKeysCommand instead of a huge authorized_keys file."
sources:
  - https://forgejo.org/docs/latest/admin/setup/recommendations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Forgejo writes every uploaded public key into the git user's `~/.ssh/authorized_keys`. sshd reads that entire file when checking whether a key is accepted, which means many read syscalls when the file is large. For instances with many users, Forgejo can instead provide keys on demand through `AuthorizedKeysCommand`:

```
Match User git
  AuthorizedKeysCommandUser git
  AuthorizedKeysCommand /usr/local/bin/forgejo --config /etc/forgejo/app.ini keys -u %u -t %t -k %k
```

Notes from the docs: sshd requires the binary to be owned by root and not writable by group or others (relevant mainly if you compile from source), and the command needs the full path to the forgejo binary, which may differ on your install. A known remaining scaling problem is that the whole Forgejo configuration is parsed on every execution, which can take a few seconds depending on the config.

Adapt the binary and config paths to your installation before use (the page says the path might differ).

## Checked

Date: 2026-11-07
Confirmed against the "Recommended Settings and Tips" page, read in full (the AuthorizedKeys command section and its code block): the default authorized_keys file in the git user's .ssh directory, sshd reading the whole file, the many read syscalls, the `Match User git` block, the root-owned binary and full-path requirements, and the remaining config parsing slowness.
Removed: the sentence explaining what `%u`, `%t` and `%k` expand to; the page shows the command but does not explain the tokens.
Method: documentation only; no commands were run.
