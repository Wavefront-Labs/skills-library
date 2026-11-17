---
id: computing-software.cloud-infrastructure-engineering.ansible.ssh-retries-timeouts-and-file-transfer-method
name: ssh-retries-timeouts-and-file-transfer-method
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, connection-plugins, ssh, ssh-retries, connection-timeout, timeout, transfer-method, sftp-scp, piped-transfer, scp-if-ssh, sftp-batch-mode, ssh-connection-section, flaky-ssh, unreachable, reconnect, ansible-ssh-retries]
level: practitioner
status: docs-checked
description: "Tune the ssh connection plugin for flaky networks and odd sshd builds: retries, connect timeout, keepalives, and transfer_method (sftp, scp, piped)."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/ssh_connection.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/connection/ssh.py", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH retries, timeouts and the file transfer method

## 1. The knobs
```ini
[defaults]
timeout = 30                 # default 10; ssh ConnectTimeout and socket read wait (seconds)

[ssh_connection]
retries = 5                  # ANSIBLE_SSH_RETRIES; retry the ssh/sftp command on rc 255
ssh_args = -o ControlMaster=auto -o ControlPersist=120s -o ServerAliveInterval=15 -o ServerAliveCountMax=3
transfer_method = smart      # smart | sftp | scp | piped
```
Per host: `ansible_ssh_retries`, `ansible_ssh_timeout`, `ansible_ssh_transfer_method`,
`ansible_ssh_args`.

- `timeout` (`-T` on the CLI) is the time to establish the SSH connection and also how long Ansible waits reading the connection once established; it is not a task time limit (use `async` or the task `timeout`).
- `retries` only retries when ssh exits **255** (connection-level failure). A module that
  fails with rc 1 is not retried; use `until`.

## 2. Transfer method
Modules and `copy`/`template` payloads are shipped with:
| Method | Command | When |
|---|---|---|
| `sftp` | `sftp -b - host` batch | default first choice in `smart` |
| `scp` | `scp` | sshd with `Subsystem sftp` disabled (some appliances, hardened images) |
| `piped` | an SSH pipe with `dd` on either side | neither sftp nor scp available |
| `smart` | try sftp, then scp, then piped | default |

```yaml
# inventory for a vendor appliance that blocks sftp
appliance1 ansible_ssh_transfer_method=piped
```
With OpenSSH 9.0 or newer clients the `scp` method needs `scp_extra_args="-O"`, according to the plugin docs; against a server with sftp disabled prefer `piped`. The `scp_if_ssh` setting does not appear among the ssh plugin options in 2.22; use `transfer_method`.

`sftp_batch_mode` (default true) runs sftp in batch mode, which allows transfer errors to be detected.

## 3. Diagnose
```bash
ansible host -m ping -vvvv 2>&1 | grep -E 'ssh|sftp|scp'
```
The `-vvvv` output shows the exact ssh command, including `ConnectTimeout`; try it by hand.

## Gotchas
- `retries` multiplies the time to detect a dead host: the plugin makes `retries + 1` attempts, each bounded by `timeout`.
- ControlPersist masters live in `control_path_dir` (default `~/.ansible/cp`); see the ControlPath length skill if paths get too long.
- Keep `smart` and override `transfer_method` only for the odd hosts.

## Verify
- [ ] Block sftp on a test host (`Subsystem sftp` commented, sshd restarted); `copy` succeeds with `transfer_method: piped` and fails with `sftp`.
- [ ] `ansible-config dump --only-changed` shows the retries/timeout values you set; `-vvvv` shows `ConnectTimeout=<timeout>` in the ssh command.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in plugins/connection/ssh.py (stable-2.22): reconnection_retries (ini retries, env ANSIBLE_SSH_RETRIES, default 0, retries only on SSH return code 255, attempts = retries + 1), timeout (default 10, env ANSIBLE_TIMEOUT or ANSIBLE_SSH_TIMEOUT, ini defaults or ssh_connection, also bounds reads), ssh_transfer_method (smart, sftp, scp, piped; default smart; var ansible_ssh_transfer_method; scp needs `scp_extra_args="-O"` on OpenSSH 9.0 and later), sftp_batch_mode default true, vars ansible_ssh_retries, ansible_ssh_timeout, ansible_ssh_args; `-T` in option_helpers.py.
- Removed unconfirmed claims: scp_if_ssh removal version, NAT/ServerAlive remark, specific ssh error strings, sftp on Win32-OpenSSH, piped speed remark, the socket length number.

Method: documentation only; no commands were run.
