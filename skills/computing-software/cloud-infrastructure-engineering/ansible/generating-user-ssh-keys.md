---
id: computing-software.cloud-infrastructure-engineering.ansible.generating-user-ssh-keys
name: generating-user-ssh-keys
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, users-groups, generate-ssh-key, ssh-keygen, openssh-keypair, authorized-key]
level: practitioner
status: docs-checked
description: "Create SSH key pairs for service users on managed hosts with user generate_ssh_key or community.crypto.openssh_keypair, then distribute the public key to other hosts."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/user.py", "https://github.com/ansible-collections/community.crypto/blob/main/plugins/modules/openssh_keypair.py", "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/authorized_key.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating user SSH keys

Use case: a service user on host A must SSH to hosts B (rsync backups, git pulls, cluster nodes).

## With the user module
```yaml
- name: Backup user with key pair
  ansible.builtin.user:
    name: backup
    generate_ssh_key: true
    ssh_key_type: ed25519
    ssh_key_file: .ssh/id_ed25519      # relative to the user's home
    ssh_key_comment: "backup@{{ inventory_hostname }}"
  register: backup_user
```
Returns `ssh_public_key` and `ssh_key_file`. It does **not** overwrite an existing key unless `force: true` is also set,
and it requires `ssh-keygen` from OpenSSH. `ssh_key_type` defaults to `rsa`, and `ssh_key_file` defaults to
`.ssh/id_rsa` (relative paths are relative to the user's home). Without `ssh_key_passphrase` the key has no passphrase.

## With community.crypto (more control)
```yaml
- community.crypto.openssh_keypair:
    path: "{{ backup_home }}/.ssh/id_ed25519"   # home from getent passwd
    type: ed25519
    owner: backup
    group: backup
    mode: "0600"
    regenerate: never          # never | fail | partial_idempotence (default) | full_idempotence | always
  register: kp
```
`regenerate: never` fails if the key cannot be read or the passphrase does not match and never regenerates an existing key;
`always` regenerates deliberately. `type` defaults to `rsa`; `ed25519` is a listed choice. The public key is written to `<path>.pub`.

## Distribute the public key
```yaml
- name: Authorise backup@A on storage hosts
  ansible.posix.authorized_key:
    user: backup
    key: "{{ hostvars[item].backup_user.ssh_public_key }}"
    key_options: 'from="{{ hostvars[item].ansible_host }}",no-agent-forwarding,no-X11-forwarding'
  loop: "{{ groups['backup_clients'] }}"
  when: inventory_hostname in groups['storage']
```
Run both in one playbook (clients play first) so `hostvars` has the registered key. You can also pin host
keys with `ansible.builtin.known_hosts` on the client.

## Gotchas
- Private keys never leave the host in this pattern; do not `fetch` them to the controller.
- Rotation: the user module does not overwrite an existing key without `force`; use `openssh_keypair` with `regenerate: always` in a dedicated rotation playbook, then redistribute.
- Supported key types depend on the `ssh-keygen` on the target (`ssh_key_type` documentation).

## Verify
- [ ] `sudo -u backup ssh -o BatchMode=yes storage1 true` succeeds from the client.

## Checked
Checked 2026-10-26 against ansible-core devel `user.py` and community.crypto `openssh_keypair.py` documentation blocks.
Confirmed: `generate_ssh_key`, `ssh_key_type` (default rsa), `ssh_key_file` (default `.ssh/id_rsa`, relative to home),
`ssh_key_comment`, `ssh_key_passphrase`, no overwrite without `force`, returned `ssh_public_key`/`ssh_key_file`,
`regenerate` choices and default, `type` choices including ed25519, `.pub` file naming. Removed unconfirmed claims: failure
without a home directory, the OpenSSH 6.5 requirement, `ansible_ssh_host_key_*` facts, and the `ssh` verification command.
Method: documentation only; no commands were run.
