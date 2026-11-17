---
id: computing-software.cloud-infrastructure-engineering.ansible.control-node-and-managed-node-requirements
name: control-node-and-managed-node-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, control-node, control-node-requirements, wsl-control-node, managed-node-requirements, libselinux-python]
level: intro
status: docs-checked
description: "Check control node and managed node prerequisites: supported OS, Python versions, WSL for Windows users, sftp/scp, and SELinux Python bindings."
sources: ["https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html", "https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html", "https://docs.ansible.com/ansible/latest/reference_appendices/faq.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/connection/ssh.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Control node and managed node requirements

Most "Ansible is broken" tickets on a new estate are really prerequisite failures. Check both ends.

## Control node
- Any UNIX-like host with a supported Python 3 (check the ansible-core support matrix: each core release supports a narrow band, e.g. core 2.17 needs control Python 3.10–3.12).
- **Windows is not a supported control node.** Use WSL2 (Ubuntu/Fedora), a Linux VM, or a container/EE. Ansible ignores an `ansible.cfg` in a world-writable current directory (and prints a warning), so keep the project in a directory only you can write to, such as the Linux filesystem under WSL.
- `ssh` client (OpenSSH) and, for password auth, `sshpass`.

```bash
python3 --version
ansible --version | head -3        # core version, config file, python used
```

## Managed nodes (Linux/UNIX)
- No agent. Needs a Python interpreter for most modules (ansible-core 2.17 and later require target Python 3.7 or newer; targets with Python 2.7 or 3.6 need core 2.16 or earlier).
- File transfer over SSH: `transfer_method` (`[ssh_connection]`, env `ANSIBLE_SSH_TRANSFER_METHOD`) is `smart` by default and tries sftp, then scp, then piped.
- SELinux-enabled hosts need the SELinux Python bindings for the interpreter Ansible uses (the FAQ mentions RHEL and Fedora).
- Exceptions: `raw` and `script` modules work without Python — use them to bootstrap.

```yaml
- hosts: new
  gather_facts: false
  tasks:
    - name: Bootstrap python where missing
      ansible.builtin.raw: test -e /usr/bin/python3 || dnf -y install python3
      changed_when: false
```

## Network and Windows targets
- Network devices: network modules do not require Python on the managed device.
- Windows: PowerShell 5.1 (PowerShell 7 LTS is also supported from ansible-core 2.21) over WinRM, PSRP or SSH; no Python.

## Gotchas
- Pin your control node Python and core together in a venv or EE; distro Python upgrades silently change what core you can run.
- If no suitable interpreter is found on a target, set `ansible_python_interpreter` per group.

## Verify
- [ ] `ansible all -m ansible.builtin.ping` succeeds for every group.
- [ ] `ansible all -m ansible.builtin.setup -a 'filter=ansible_selinux'` returns without the bindings error.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/installation_guide/intro_installation.rst: UNIX-like control node, Windows only via WSL, managed nodes need Python and an SSH account with a POSIX shell, network modules need no Python; in release_and_maintenance.rst: Python support ranges (2.17 control 3.10-3.12, target 3.7-3.12; Python 2.7 and 3.6 targets only up to 2.16), PowerShell 5.1 and 7 LTS from 2.21.
- Confirmed in modules/raw.py and script.py that both work without Python; in plugins/connection/ssh.py that transfer_method defaults to smart (sftp, scp, piped); in config/manager.py that a world-writable working directory is skipped for ansible.cfg; in the FAQ that SELinux bindings are needed on SELinux-enabled RHEL and Fedora.
- Removed unconfirmed claims: package names and exact SELinux error text, .NET version, WSL key-permission remark.

Method: documentation only; no commands were run.
