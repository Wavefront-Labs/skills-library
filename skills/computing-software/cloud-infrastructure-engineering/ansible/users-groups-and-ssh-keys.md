---
id: computing-software.cloud-infrastructure-engineering.ansible.users-groups-and-ssh-keys
name: users-groups-and-ssh-keys
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, users, groups, user-module, group-module, authorized-key, ssh-keys, password-hash, sudoers, community-general-sudoers, getent, uid-gid, system-accounts, locked-accounts, expire, remove-users, offboarding, ssh-ca, known-hosts, login-policy]
level: practitioner
status: docs-checked
description: "Manage Linux users and groups with Ansible: fixed UIDs/GIDs, hashed passwords, authorized_key with exclusive mode, sudoers drop-ins validated by visudo, locking and removing leavers, getent checks."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/posix/authorized_key_module.html", "https://docs.ansible.com/ansible/latest/collections/community/general/sudoers_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/user.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/getent.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/known_hosts.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/sudoers.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_filters.rst", "https://github.com/openssh/openssh-portable/blob/master/sshd_config.5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Users, groups and SSH keys

**Goal:** every host has the same accounts, UIDs, keys and sudo rights as the data
says — no more, no fewer — and offboarding is one line removed from a list.

## 1. Data-driven accounts
```yaml
# group_vars/all/users.yml
managed_users:
  - {name: alice, uid: 2001, groups: [wheel, developers], keys: ["ssh-ed25519 AAAA... alice@laptop"], state: present}
  - {name: bob,   uid: 2002, groups: [developers], keys: [], state: absent}
managed_groups:
  - {name: developers, gid: 3001}
```
```yaml
- ansible.builtin.group: {name: "{{ item.name }}", gid: "{{ item.gid }}", state: present}
  loop: "{{ managed_groups }}"
- ansible.builtin.user:
    name: "{{ item.name }}"
    uid: "{{ item.uid }}"
    groups: "{{ item.groups | default([]) }}"
    append: false                    # groups list is authoritative
    shell: /bin/bash
    password: "{{ item.password_hash | default(omit) }}"   # a pre-hashed value; omitted when absent
    update_password: on_create       # only set the password for newly created users
    state: "{{ item.state }}"
    remove: "{{ item.state == 'absent' }}"   # delete home/mail on removal
  loop: "{{ managed_users }}"
  loop_control: {label: "{{ item.name }}"}
- ansible.posix.authorized_key:
    user: "{{ item.name }}"
    key: "{{ item.keys | join('\n') }}"
    exclusive: true                  # all other keys are removed
  loop: "{{ managed_users | selectattr('state', 'equalto', 'present') | list }}"
  loop_control: {label: "{{ item.name }}"}
```
- Fixed `uid`/`gid` keep NFS and container volumes sane across hosts.
- `exclusive: true` removes every key not in the single `key` string, including keys added by hand, so use it only
  on accounts Ansible fully owns.
- `system: true` + `create_home: false` + a nologin `shell` suit service accounts.

## 2. Passwords
Hash on the control node, never pass clear text:
```yaml
password: "{{ vault_alice_pw | password_hash('sha512', 65534 | random(seed=inventory_hostname) | string) }}"
```
The filter docs derive a stable salt with `random(seed=inventory_hostname)`; they also say `password_hash` depends on
`passlib`, with the `crypt` module as a fallback, and that results differ depending on whether passlib is installed.
`password_lock: true` locks the password without changing the hash; a negative `expires` removes the expiry;
`password_expire_max` is the maximum days between password changes (Linux only). The module writes the `password` value
to `/etc/shadow` without validation.

## 3. sudo
```yaml
- community.general.sudoers:
    name: developers-restart
    user: "%developers"
    commands: [/usr/bin/systemctl restart app]
    nopassword: true
    validation: required            # visudo must be available to validate the rule (default: detect)
# or a template:
- ansible.builtin.template: {src: sudoers.j2, dest: /etc/sudoers.d/90-ansible, mode: "0440", validate: /usr/sbin/visudo -csf %s}
```
`community.general.sudoers` uses `name` as the file name of the sudoers file for the rule, and `nopassword` defaults to `true`. The module docs for `copy` use `validate: /usr/sbin/visudo -csf %s` for sudoers files. Keep the automation account's own rule in a separate file.

## 4. Checks
```yaml
- ansible.builtin.getent: {database: passwd, key: alice}
- ansible.builtin.debug: {var: ansible_facts.getent_passwd}
- ansible.builtin.command: id alice
  changed_when: false
```

## 5. Known hosts and host keys
`ansible.builtin.known_hosts` (`name`, `key`, `path` default `~/.ssh/known_hosts`) manages entries that pin outbound SSH trust for deploy users.
For inbound trust at scale, sshd supports `TrustedUserCAKeys` in `sshd_config` (see sshd_config(5)).

## Gotchas
- `groups:` without `append: true` replaces supplementary groups; from Ansible 2.21 `append` is required when `groups` is set. Decide which is authoritative and be consistent.
- `state: absent` with `force: true` behaves like `userdel --force`; `remove: true` like `userdel --remove`.
- `home:` on an existing user does not move the old home unless `move_home: true`.
- `local: true` forces the "local" command alternatives (for example `luseradd`) for centrally authenticated environments.

## Verify
- [ ] `getent` (database `passwd`, key `alice`) shows uid 2001 on every host.
- [ ] `sudo -l -U alice` on a host lists exactly the intended commands.
- [ ] Setting a user to `state: absent` removes the account, home and key file on the next run; the second run is `changed=0`.

## Checked
Checked 2026-10-26 against ansible-core devel `user.py`, `getent.py`, `known_hosts.py`, `copy.py` (visudo example),
ansible.posix `authorized_key.py`, community.general `sudoers.py`, ansible-documentation `playbooks_filters.rst`
and OpenSSH `sshd_config.5`. Confirmed: `update_password`, `password_lock`, `expires`, `password_expire_max`, shadow write
without validation, `append` requirement from 2.21, `exclusive` behaviour, `sudoers` `validation`/`nopassword`/`name`,
`known_hosts` options, `TrustedUserCAKeys`, `random(seed=...)` and passlib notes. Removed unconfirmed claims: `!` meaning
for default passwords, "never edit /etc/sudoers" rule, process-in-use messages, key whitespace churn, chown recipe,
LDAP/SSSD shadowing, and the ad hoc verification form.
Method: documentation only; no commands were run.
