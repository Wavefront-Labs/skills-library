---
id: computing-software.cloud-infrastructure-engineering.ansible.connection-plugins-and-ssh-pipelining
name: connection-plugins-and-ssh-pipelining
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, connection-plugins, connection-plugin, ssh, ssh-pipelining, pipelining, controlpersist, control-master, paramiko, local-connection, community-docker, docker-connection, podman-connection, winrm, psrp, ansible-ssh-common-args, proxyjump, jump-host, bastion, requiretty, ssh-args, ansible-connection]
level: practitioner
status: docs-checked
description: "Choose and tune Ansible connection plugins: ssh with pipelining and ControlPersist, bastion/ProxyJump, local, docker/podman, psrp for Windows; fix requiretty, host key and slow-connection failures."
sources: ["https://docs.ansible.com/ansible/latest/inventory_guide/connection_details.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/connection/ssh.py", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://github.com/ansible-collections/community.docker/blob/main/plugins/connection/docker.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection plugins and SSH pipelining

**Goal:** every host is reached with the right transport, the transport is as fast as it
can be, and a connection failure says what is wrong.

## 1. Pick the plugin per host or group
Set `ansible_connection` in inventory:
| Value | Target | Notes |
|---|---|---|
| `ssh` (default) | Linux/BSD/macOS via OpenSSH client | fastest, honours `~/.ssh/config` |
| `paramiko` | removed from ansible-core in 2.21 (it is not in the 2.22 plugin list); only present on 2.20 and earlier | |
| `local` | run on the control node itself (`localhost` is implicit) | `delegate_to: localhost` uses it too |
| `community.docker.docker` | running containers | `ansible_host` = container name |
| `winrm` / `psrp` | Windows | both ship in ansible-core |
| `ansible.netcommon.network_cli` / `netconf` / `httpapi` | network devices | see network automation skill |

## 2. The ssh plugin, tuned
```ini
[ssh_connection]
pipelining = True
ssh_args = -C -o ControlMaster=auto -o ControlPersist=60s -o ServerAliveInterval=30
```
- **Pipelining** (default off; accepted under `[defaults]`, `[connection]` or `[ssh_connection]`, env `ANSIBLE_PIPELINING`) executes modules without a separate file transfer, which can be a large speed-up. It conflicts with privilege escalation: with `sudo` you must first disable `requiretty` in sudoers on the managed hosts. It is switched off while `ANSIBLE_KEEP_REMOTE_FILES` is on.
- **ControlPersist** keeps the master socket open. The default `ssh_args` is `-C -o ControlMaster=auto -o ControlPersist=60s`, and when `control_path` is unset Ansible generates a short hashed socket name inside `control_path_dir` (default `~/.ansible/cp`). If socket paths still get too long, set `control_path_dir` to a shorter directory.
- Setting `ssh_args` replaces that default string (including `-C`), while `ssh_common_args` and `ssh_extra_args` add to it. Use the append variants in inventory (`ansible_ssh_common_args`).

### Bastion / jump host
```yaml
# group_vars/private_subnet.yml
ansible_ssh_common_args: '-o ProxyJump=bastion.example.com'
```
Or put a `Host 10.0.*` + `ProxyJump` stanza in `~/.ssh/config`; the ssh plugin reads it.
`ProxyCommand` style works too but `ProxyJump` needs no `nc` on the bastion.

### Host keys
`host_key_checking` defaults to True; `host_key_checking = False` is a lab-only shortcut. In production pre-seed `known_hosts` and keep checking on. A host with a changed key causes an error until corrected, and an unknown host may prompt interactively, which is awkward under cron.

## 3. Other connection variables
`ansible_host`, `ansible_port`, `ansible_user`, `ansible_ssh_private_key_file`,
`ansible_password` (use vault), `ansible_become*`, `ansible_python_interpreter`,
`ansible_shell_type` (shell plugins in ansible-core 2.22: `sh`, `powershell`, `cmd`), `ansible_ssh_executable`.

## 4. Diagnosing
```bash
ansible host -m ping -vvvv            # prints the exact ssh command line
ANSIBLE_SSH_ARGS="-vv" ansible host -m ping   # OpenSSH's own debug
ansible-config dump -t connection | grep -i -E 'pipelining|ssh_args|control_path'
```
Common symptoms:
- Permission denied (publickey) → wrong `ansible_user` or key; try the printed ssh command by hand.
- A timeout waiting for the privilege escalation prompt → missing become password, or pipelining with `requiretty`.
- An interpreter-not-found error from the remote shell → set `ansible_python_interpreter`, or use the `raw` module to install Python.
- A ControlPath-too-long error → shorten `control_path_dir`.

## Gotchas
- `timeout` (default 10, `[defaults]` or `[ssh_connection]`, env `ANSIBLE_TIMEOUT`) is the SSH connection wait time, not a task timeout; raise it for slow bastions and use `ansible.builtin.wait_for_connection` after reboots.

## Verify
- [ ] `ansible all -m ping -o` succeeds for every group, each with the intended `ansible_connection`.
- [ ] `ansible-config dump --only-changed` shows `ANSIBLE_PIPELINING: True`.
- [ ] No host has `host_key_checking` disabled in production inventory or config.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in plugins/connection/ssh.py (stable-2.22): ssh_args default `-C -o ControlMaster=auto -o ControlPersist=60s`, ssh_common_args/ssh_extra_args, control_path null default (hashed name), control_path_dir default ~/.ansible/cp, host_key_checking default True, timeout default 10 with ini in defaults and ssh_connection, pipelining ini sections and env names.
- Confirmed in config/base.yml: ANSIBLE_PIPELINING default False, requiretty note, disabled with keep remote files. Confirmed in the connection-plugin directory listing that ansible-core 2.21 and 2.22 ship only local, psrp, ssh and winrm (changelog v2.21: paramiko connection plugin removed), and that shell plugins are sh, powershell and cmd.
- Confirmed in docs/docsite/rst/inventory_guide/connection_details.rst: host key behaviour and ProxyJump via ssh config.
- Removed unconfirmed claims: paramiko details, podman plugin and Molecule, Mitogen, specific error strings and the socket length limit, localhost become remark, speed claims.

Method: documentation only; no commands were run.
