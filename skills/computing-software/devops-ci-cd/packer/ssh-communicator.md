---
id: computing-software.devops-ci-cd.packer.ssh-communicator
name: ssh-communicator
category: computing-software
field: devops-ci-cd
product: packer
tags: [ssh, communicator, ssh-username, timeout, comm-ssh]
level: practitioner
status: docs-checked
description: "Configure the SSH communicator: required username, port 22, timeouts, handshake attempts, pty and file transfer method."
sources:
  - "https://developer.hashicorp.com/packer/docs/communicators/ssh/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

SSH is the default communicator for a majority of builders. Packer connects to the booted machine over SSH to run provisioners.

```hcl
source "happycloud" "example" {
  communicator = "ssh"
  ssh_host     = "127.0.0.1"
  ssh_username = "packer"
  ssh_password = "packer"
}
```

Settings and defaults from the docs:

- `ssh_username` is required.
- `ssh_host` is the address; many builders fill it in.
- `ssh_port` defaults to 22.
- `ssh_password` or a key; `ssh_timeout` is the wait for SSH to become available, default `5m` unless `ssh_handshake_attempts` is set.
- `ssh_handshake_attempts` defaults to 10, unless `ssh_timeout` is set.
- `ssh_pty` defaults to false.
- `ssh_keep_alive_interval` defaults to 5s (negative disables); `ssh_read_write_timeout` is how long to wait for a remote command to end, disabled by default.
- `ssh_file_transfer_method` is `scp` (default) or `sftp`.
- `ssh_clear_authorized_keys` tries to remove Packer's temporary key from `authorized_keys`; mostly cosmetic and needs `sed` on the guest.
- `ssh_disable_agent_forwarding` turns off agent forwarding.
- `ssh_ciphers`, `ssh_key_exchange_algorithms` and `ssh_certificate_file` adjust cryptography.

## Checked
2026-11-03. Confirmed against the SSH communicator page: option names and defaults (`ssh_port`, `ssh_timeout`, `ssh_handshake_attempts`, `ssh_pty`, keep-alive, read/write timeout, file transfer method), required username and the cryptography options. Removed the unsourced troubleshooting advice and changed the example to a placeholder builder.
Method: documentation only; no commands were run.
