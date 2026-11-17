---
id: computing-software.devops-ci-cd.rundeck.ssh-node-authentication-precedence
name: ssh-node-authentication-precedence
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, ssh-node-execution, ssh-authentication, ssh-key-storage-path, sftp-file-copier]
level: practitioner
status: docs-checked
description: "Configure Rundeck SSH node execution: hostname and username, private key or password auth, key storage paths, timeouts and the node, project, framework precedence."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/projects/node-execution/ssh.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SSH is the default node executor and SCP the default file copier. The recommended plugin suite, SSH-J, is the default for new projects. A node needs `hostname` (`host:port`, default port 22) and `username`.

Every setting resolves in this order, first match wins: node attribute, then `project.<name>` in `project.properties`, then `framework.<name>` in `framework.properties`.

| Setting | Node attribute |
|---|---|
| auth mode (`password` or `privateKey`, default) | `ssh-authentication` |
| key file on disk | `ssh-keypath` |
| key in Key Storage | `ssh-key-storage-path` |
| timeouts in ms, 0 = indefinite | `ssh-connection-timeout`, `ssh-command-timeout` |
| SSH config option | `ssh-config-KEY` |

Username order: node `username` (may hold `${job.username}` or `${option.someUsername}`), then `project.ssh.user`, then `framework.ssh.user`.

Key Storage paths live under `keys/` and may embed `${job.project}`. If both a storage path and another option are set, the storage path is used.

Passphrase-protected keys: use a Secure Remote Authentication job option (prompted per run, not stored) or a stored passphrase.

SFTP instead of SCP: Project Settings, Edit Configuration, Default File Copier, choose SSHJ-SCP, tick Use SFTP.

Defaults: `PreferredAuthentications: publickey,password,keyboard-interactive`, `MaxAuthTries: 1`.

## Checked

2026-11-04: defaults, precedence, attribute names, timeouts, username order, key storage rules, passphrase options, SFTP steps and SSH config defaults confirmed against the SSH Node Execution page. Removed the unsourced Verify line.
Method: documentation only; no commands were run.
