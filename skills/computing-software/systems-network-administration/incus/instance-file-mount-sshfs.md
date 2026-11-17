---
id: computing-software.systems-network-administration.incus.instance-file-mount-sshfs
name: instance-file-mount-sshfs
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, file-mount, sshfs, sftp, listen, auth-user]
level: practitioner
status: docs-checked
description: "Mount an Incus instance directory locally with incus file mount (sshfs), or start an SFTP listener with --listen and --auth-user and connect with sshfs."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_access_files.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mount instance files with sshfs

Direct mount (needs `sshfs` installed):
```
incus file mount <instance>/<path_to_directory> <local_location>
```

SFTP listener instead:
```
incus file mount <instance> [--listen <address>:<port>] [--auth-user <name>]
sshfs <user_name>@<address>:<path_to_directory> <local_location> -p <port>
```

- Without `--listen`, Incus picks a random local port (on 127.0.0.1).
- `--listen <address>:0` binds a chosen address with a random port.
- Without `--auth-user`, a user name is generated. The command prints port, user name and password.
- Binding a non-local address exposes the instance remotely; be careful.
- VMs need the `incus-agent` running.

## Checked

2026-11-04: confirmed against the Incus access-files how-to (`file mount` with sshfs, SFTP listener, `--listen`, `--auth-user`, printed credentials, exposure warning). Nothing removed.

Method: documentation only; no commands were run.
