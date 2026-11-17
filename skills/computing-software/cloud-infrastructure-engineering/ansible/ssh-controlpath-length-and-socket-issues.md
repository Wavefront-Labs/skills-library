---
id: computing-software.cloud-infrastructure-engineering.ansible.ssh-controlpath-length-and-socket-issues
name: ssh-controlpath-length-and-socket-issues
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, performance-tuning, control-path, controlpersist, ssh-connection-section]
level: practitioner
status: docs-checked
description: "Fix ControlPath too long and stale socket errors: control_path and control_path_dir settings, hashed %C paths, shared filesystems and cleanup of multiplexing sockets."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/ssh_connection.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/connection/ssh.py", "https://man.openbsd.org/ssh_config", "https://man.openbsd.org/ssh"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ControlPath length and socket issues

With ControlPersist, OpenSSH keeps a master socket per host. Unix socket paths have a small length limit; long hostnames, usernames and home directories can exceed it.

## Symptoms
- OpenSSH refuses a ControlPath that is too long for a Unix domain socket.
- Sockets can go stale after network changes, VPN reconnects or a killed run.

## Fix length: hashed path
```ini
[ssh_connection]
control_path_dir = ~/.ansible/cp
control_path = %(directory)s/%%C          # %C = hash of %l%h%p%r%j (ssh_config), so the name stays short
```
When `control_path` is unset (the default), Ansible generates a short hashed name inside `control_path_dir` (default `~/.ansible/cp`), so problems usually come from an override in ansible.cfg or `~/.ssh/config`. The plugin ignores `control_path` if `-o ControlPath` is set in the ssh args. The ssh_config manual recommends a ControlPath that includes at least %h, %p and %r (or %C) in a directory not writable by others. Ansible's own examples double the percent signs in ansible.cfg (`%%h`).

Short dir option: point `control_path_dir` at a short local directory that other users cannot write to.

## Stale sockets
```bash
ssh -O check -o ControlPath=~/.ansible/cp/<hash> host
ssh -O exit  -o ControlPath=~/.ansible/cp/<hash> host
rm -f ~/.ansible/cp/*          # when no runs are active
```
Sockets go stale after network changes, VPN reconnects, or a killed run; `meta: reset_connection` closes them inside a play.

## Gotchas

## Verify
```bash
ansible host -m ansible.builtin.ping -vvvv 2>&1 | grep -o 'ControlPath=[^ ]*'
```

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in plugins/connection/ssh.py (stable-2.22): control_path default null with an Ansible-generated hash (first 10 hex digits of a SHA-1 of host, port and user), control_path_dir default ~/.ansible/cp, control_path ignored when -o ControlPath is in the ssh args, ControlPersist default 60s in ssh_args.
- Confirmed in ssh_config(5) and ssh(1) from openssh-portable master: %C is the hash of %l%h%p%r%j, the recommendation to include %h %p %r or %C in a directory not writable by others, and the `-O check` and `-O exit` multiplexing commands; in modules/meta.py that `reset_connection` interrupts a persistent ssh ControlPersist connection.
- Removed unconfirmed claims: exact socket length numbers, specific error strings, the NFS/CIFS section, the execution-environment and ControlMaster=no remarks.

Method: documentation only; no commands were run.
