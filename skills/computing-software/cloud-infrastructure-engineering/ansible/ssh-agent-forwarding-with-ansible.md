---
id: computing-software.cloud-infrastructure-engineering.ansible.ssh-agent-forwarding-with-ansible
name: ssh-agent-forwarding-with-ansible
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, connection-plugins, agent-forwarding, ssh-agent, git-clone]
level: practitioner
status: docs-checked
description: "Forward the SSH agent through Ansible so managed nodes can git clone private repos or hop onward, with become-safe socket handling and security limits."
sources: ["https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/connection/ssh.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/git.py", "https://docs.ansible.com/ansible/latest/inventory_guide/connection_details.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSH agent forwarding

Use case: managed hosts clone a private git repo with **your** key, without copying private keys to servers.

## Enable
```ini
# ansible.cfg
[ssh_connection]
ssh_args = -C -o ControlMaster=auto -o ControlPersist=60s -o ForwardAgent=yes
```
or per group: `ansible_ssh_extra_args: '-o ForwardAgent=yes'` (the `ssh_args` default is `-C -o ControlMaster=auto -o ControlPersist=60s`, and setting `ssh_args` replaces it). Load the key locally: `ssh-add ~/.ssh/deploy_ed25519; ssh-add -l`.

## Use it
```yaml
- name: Clone private repo with forwarded agent
  ansible.builtin.git:
    repo: git@github.com:org/app.git
    dest: /opt/app
    version: v1.4.2
    accept_newhostkey: true   # needs OpenSSH 7.5 or later on the host
```

## become breaks it
The forwarded agent socket belongs to the connecting user's session, and a task run with `become` runs as another user with its own environment, so test whether the agent is still reachable under `become`. A safe pattern is to run the git task without become into a directory the connecting user owns, then fix ownership.

## ControlPersist gotcha
An existing multiplexed master connection created **without** forwarding is reused; forwarding does not appear until it expires. Wait for `ControlPersist` to time out after changing args, or close the master with `ssh -O exit` (the socket location is the `control_path` option; by default Ansible generates a unique hash).

## Security
Anyone with root on the target can use your agent while connected. Prefer a read-only **deploy key** on the server (or a short-lived token over HTTPS) for production; reserve forwarding for dev/bastion hops.

## Verify
```bash
ansible host -m ansible.builtin.shell -a 'ssh-add -l'      # lists your key fingerprint
```

## Checked

Checked 2026-10-26 against the ansible-core `ssh` connection plugin and `git` module sources (devel). Confirmed: `ssh_args` default `-C -o ControlMaster=auto -o ControlPersist=60s`; `ssh_extra_args` / `ansible_ssh_extra_args`; `control_path` generates a unique hash when unset and is ignored if `-o ControlPath` is in the ssh args; `git` `accept_newhostkey` (OpenSSH 7.5 or later). Removed the sudoers `env_keep` advice, the `~/.ansible/cp` path and the `ssh-add -c` remark, which no Ansible page confirms.

Method: documentation only; no commands were run.
