---
id: computing-software.cloud-infrastructure-engineering.ansible.user-shell-home-and-supplementary-groups
name: user-shell-home-and-supplementary-groups
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, users-groups, home-directory, user-shell, append-groups, supplementary-groups, system-users]
level: intro
status: docs-checked
description: "Set a user's shell, home directory, primary and supplementary groups with ansible.builtin.user, using append to avoid stripping existing groups, and create system accounts."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/group_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/user.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/group.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User shell, home and supplementary groups

## Supplementary groups: append or replace
```yaml
- name: Ensure groups exist
  ansible.builtin.group: {name: "{{ item }}", state: present}
  loop: [developers, docker]

- name: Add alice to developers and docker, keep her other groups
  ansible.builtin.user:
    name: alice
    groups: [developers, docker]
    append: true
```
`append` defaults to false: the user is then only in the groups listed in `groups` and is removed from all others.
Use replace semantics only when this task is the single source of truth for her groups. The docs state that from
Ansible 2.21 `append` is required whenever `groups` is specified, so set it explicitly.
`groups: ''` removes the user from all groups except the primary group.

Primary group: `group: developers`. The group must exist first.

## Shell and home
```yaml
- name: Interactive user
  ansible.builtin.user:
    name: bob
    shell: /bin/zsh            # the shell must be installed on the host
    home: /srv/users/bob
    create_home: true
    move_home: true            # with home: try to move the old home directory to the new path
    skeleton: /etc/skel
    comment: "Bob Jones"

- name: Service account, no login
  ansible.builtin.user:
    name: app
    system: true               # system account (cannot be changed on existing users)
    shell: /usr/sbin/nologin   # path varies by distribution
    home: /opt/app
    create_home: false
```
`uid` sets the UID (and `ansible.builtin.group` has `gid`); pin them when files are shared across hosts.

## Removing users
```yaml
- ansible.builtin.user:
    name: olduser
    state: absent
    remove: true       # attempt to remove directories associated with the user (like userdel --remove)
```
Lock instead of delete for audit: `password_lock: true` locks the password only (it does not disable the user), and
`expires` takes an epoch time (a negative value removes the expiry) on GNU/Linux, FreeBSD and DragonFlyBSD.

## Gotchas
- `skeleton` requires `create_home`.
- `state: absent` with `force: true` behaves like `userdel --force`; check the userdel man page on your system.
- `shell` is a path type from 2.18; when unset, the default comes from the underlying tool (see the module's Notes).

## Verify
- [ ] `id alice` shows all expected groups (old ones retained with `append: true`).
- [ ] `getent passwd bob` shows the shell and home.

## Checked
Checked 2026-10-26 against ansible-core devel `user.py` and `group.py` documentation blocks (repository last commit
2026-10-23). Confirmed: `groups`/`append` semantics including the requirement of `append` from 2.21, `groups: ''`,
`shell`, `home`, `move_home`, `create_home`, `skeleton`, `system`, `remove`, `force`, `password_lock`, `expires`.
Removed unconfirmed claims: usermod process-in-use message, session effect of group changes, `chown` recipe, NFS advice,
RHEL nologin path.
Method: documentation only; no commands were run.
