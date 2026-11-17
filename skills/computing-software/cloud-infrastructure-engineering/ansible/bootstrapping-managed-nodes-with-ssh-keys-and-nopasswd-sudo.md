---
id: computing-software.cloud-infrastructure-engineering.ansible.bootstrapping-managed-nodes-with-ssh-keys-and-nopasswd-sudo
name: bootstrapping-managed-nodes-with-ssh-keys-and-nopasswd-sudo
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, managed-nodes, ssh-keys, key-distribution, nopasswd, sudoers-automation, automation-user, bootstrap-playbook, ask-pass, first-contact, node-onboarding]
level: practitioner
status: docs-checked
description: "Bring a fresh host under Ansible: create the automation user, distribute the control-node key, install a validated sudoers drop-in, then prove key-only become works."
sources: ["https://docs.ansible.com/ansible/latest/inventory_guide/connection_details.html#setting-up-ssh-keys", "https://docs.ansible.com/ansible/latest/collections/ansible/posix/authorized_key_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html", "https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_lookup.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/ssh_connection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootstrapping managed nodes with SSH keys and NOPASSWD sudo

**Goal:** after one password-driven run, every later run is key-based and `become` needs no
password. The bootstrap play runs once per host with `-k -K` (`--ask-pass`, `--ask-become-pass`).

## 1. Control-node key
Generate an SSH key pair on the control node (one per control node or CI runner, never a shared
personal key), then point Ansible at the private key:
```ini
# ansible.cfg
[defaults]
remote_user = automation
private_key_file = /path/to/ansible_key
```
`private_key_file` under `[defaults]` is the ssh connection plugin's INI entry; the CLI form is
`--private-key`, the variable form is `ansible_private_key_file`. The `remote_user` setting is
also under `[defaults]` (CLI `--user`, keyword `remote_user`, variable `ansible_user`). If the key
has a passphrase, Ansible cannot prompt for it with the ssh connection plugin: use `ssh-agent`.

## 2. The bootstrap play (run with the initial admin credentials)
`ansible.posix.authorized_key` is not part of ansible-core: install the `ansible.posix` collection.
```yaml
- name: Bootstrap hosts for Ansible
  hosts: new_hosts
  remote_user: "{{ bootstrap_user | default('root') }}"
  become: true
  gather_facts: false
  tasks:
    - name: Automation user
      ansible.builtin.user:
        name: automation
        shell: /bin/bash
        groups: "{{ automation_groups }}"   # your distro's admin group(s)
        append: true

    - name: Authorized key
      ansible.posix.authorized_key:
        user: automation
        key: "{{ lookup('ansible.builtin.file', '/path/to/ansible_key.pub') }}"
        exclusive: true            # only this key; use false while rotating

    - name: Password-less sudo, validated before install
      ansible.builtin.copy:
        dest: /etc/sudoers.d/90-automation
        content: |
          automation ALL=(ALL) NOPASSWD: ALL
        owner: root
        group: root
        mode: "0440"
        validate: /usr/sbin/visudo -csf %s
```
```bash
ansible-playbook bootstrap.yml -i new_hosts.ini -k -K -e bootstrap_user=admin
```

## Notes on the modules used
- `lookup('ansible.builtin.file', ...)` reads the file on the Ansible controller, so the public key is read from the control node.
- `authorized_key`: `exclusive` removes every non-specified key from `authorized_keys` and defaults to false; it is not loop aware (exclusive per loop iteration), so pass all keys in one `key` string separated by newlines. `state` defaults to `present`; `manage_dir` defaults to true, and the docs say to set it false when using an alternate `path`.
- `user`: `groups` replaces all other supplementary groups unless `append: true`. The docs say that from Ansible 2.21 `append` is required when `groups` is specified.
- `copy` with `validate`: the command runs against a temporary file whose path replaces `%s`, and shell features such as pipes and expansion do not work in it. The module docs' own example uses `validate: /usr/sbin/visudo -csf %s`.
- `copy` with `mode`: quote it (`"0440"`) so Ansible does not read a decimal number.
- Rotation: run the play with a new key and `exclusive: false`, then remove the old key by a run with `exclusive: true` or `state: absent`.

## Gotchas
- Always `validate` anything written to sudoers: a typo can lock out sudo. Check the sudoers(5) and visudo manuals on the target for file-naming and `Defaults` rules; this skill does not restate them.
- `exclusive: true` wipes other keys the admin team relies on; agree on it before running.
- Narrowing the sudo rule to a command list is a site-policy decision; check it against your modules before relying on it.

## Verify
- [ ] `ansible new_hosts -m ansible.builtin.ping` succeeds without `-k` (the ping module reports `pong` on success).
- [ ] `ansible new_hosts -b -m ansible.builtin.command -a id` succeeds without `-K`.

## Checked
Date: 2026-11-07. Pages read in full: Connection methods and details (the whole page, including "Setting up SSH keys"), ansible.posix.authorized_key, ansible.builtin.copy, ansible.builtin.user (searched the parameters `groups`, `append`, `shell`, `name`, not read in full), ansible.builtin.file lookup, ansible.builtin.ping and ansible-playbook CLI. The ssh connection plugin page was read for the `private_key_file` and `remote_user` entries only (searched, not read in full). Confirmed: `-k`/`--ask-pass`, `-K`/`--ask-become-pass`, `-i`, `-e`, `--private-key`, authorized_key parameters and defaults, `validate` semantics and `%s`, the `visudo -csf %s` example, `mode` quoting.
Removed as not on a cited page: `ssh-keygen` flags, `ssh-copy-id`, the `requiretty` setting, the claim that sudoers.d files with `.` or `~` are ignored, the narrow-sudo-rule example, the AnsiballZ path, `log_output`/`iolog_dir`, the sshd hardening task and handler, the `visudo -cf` form (the docs show `-csf`), the distro-specific `wheel`/`sudo` group expression, sample `uid=0(root)` output, and the `ssh ... sudo -n true` verify step.
Method: documentation only; no commands were run.
