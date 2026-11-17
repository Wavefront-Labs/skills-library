---
id: computing-software.cloud-infrastructure-engineering.ansible.dnf-module-streams-and-package-groups
name: dnf-module-streams-and-package-groups
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, packages-repos, dnf-module-streams, package-groups, dnf, appstream, rhel]
level: practitioner
status: docs-checked
description: "Install RHEL AppStream module streams and package groups with ansible.builtin.dnf (@module:stream, @group), switch streams safely, and check the result."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/dnf_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/dnf.py", "https://github.com/rpm-software-management/dnf/blob/master/doc/command_ref.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnf module streams and package groups

## Package groups
```yaml
- name: Install development tools group
  ansible.builtin.dnf:
    name: "@Development Tools"       # group name or id: "@development"
    state: present
```
The module documentation's example installs the group `@Development tools`. It also warns that group removal
does not work if the group was installed with Ansible, because the dnf API does not mark such groups as installed.

## Module streams (RHEL 8/9 AppStream)
```yaml
- name: Install PostgreSQL 15 stream, server profile
  ansible.builtin.dnf:
    name: "@postgresql:15/server"     # @module:stream/profile
    state: present
```
The docs show `@postgresql:9.6/client` (stream and profile), `@postgresql:9.6` (stream only) and
`@postgresql/client` (profile only).

Switching streams (e.g. nodejs 18 → 20):
```yaml
- ansible.builtin.command: dnf -y module reset nodejs
  changed_when: true
- ansible.builtin.dnf:
    name: "@nodejs:20"
    state: present
```
The module documentation shows no option to reset a stream, so the reset above uses `command` (`dnf module reset <module-name>` is
documented in the dnf command reference); `state: absent` removes packages.

## Pinning and other options
- `name: postgresql-server-15.4*` for version globs; `allow_downgrade: true` when pinning down.
- `enablerepo` takes repo ids and applies for that transaction only.
- `install_weak_deps` defaults to `true`; set `false` to skip weak dependencies.
- `ansible.builtin.package_facts` is the documented alternative to the `list` option for querying packages.

## Gotchas
- A stream enabled by hand on some hosts and not others is drift; audit with `dnf module list --enabled`.

## Verify
- [ ] `dnf module list --enabled postgresql` lists stream 15 as enabled (`module list --enabled` is in the dnf command reference).

## Checked
Checked 2026-10-26 against ansible-core devel `lib/ansible/modules/dnf.py` (options and examples). Confirmed the
`@group`, `@module:stream/profile`, `@module:stream` and `@module/profile` forms, `allow_downgrade`, `enablerepo`,
`install_weak_deps` default, the group-removal note. Removed unconfirmed claims: environment-group `@^` syntax,
dnf5 commands, `--with-optional` advice, RHEL 10 module-stream statement (Red Hat docs are not readable in this lane),
default-stream behaviour, locale note and the `crb` repository advice. Red Hat source link dropped.
Method: documentation only; no commands were run.
