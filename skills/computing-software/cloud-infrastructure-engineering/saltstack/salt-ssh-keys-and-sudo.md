---
id: computing-software.cloud-infrastructure-engineering.saltstack.salt-ssh-keys-and-sudo
name: salt-ssh-keys-and-sudo
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, salt-ssh, ssh-keys, sudo, ssh-copy-id, nopasswd]
level: practitioner
status: docs-checked
description: "Authenticate salt-ssh with its generated key pair, deploy the public key with ssh-copy-id, and enable sudo in the roster with NOPASSWD."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/ssh/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# salt-ssh keys and sudo

Keys: omit `passwd` in the roster and salt-ssh uses a key pair it generates on first run at `/etc/salt/pki/master/ssh/salt-ssh.rsa`. Deploy the public key to a target:

```
ssh-copy-id -i /etc/salt/pki/master/ssh/salt-ssh.rsa.pub user@server.demo.com
```

Sudo: set `sudo: True` in the roster (off by default). It only works if the user has NOPASSWD in sudoers, for example:

```
fred ALL=(ALL) NOPASSWD: ALL
```

Agent forwarding: setting `priv` to `agent-forwarding` uses ssh agent forwarding (see the roster options skill).

Non-root operators: set `pki_dir` and `cachedir` to writable paths and point to a private config directory with `-c`.

Debugging: run `salt-ssh` with `-ltrace`, find `SALT_ARGV` to see the underlying `salt-call` command, and drop `-l quiet`, `--metadata` and `--output json` to get more detail.

## Checked

2026-11-04: read the Salt SSH page in full. Confirmed the generated key path and first-run generation, ssh-copy-id usage, sudo and the NOPASSWD note, agent forwarding, the non-root pki_dir, cachedir and -c advice, and the -ltrace SALT_ARGV debugging steps. Nothing removed.

Method: documentation only; no commands were run.

