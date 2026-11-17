---
id: computing-software.cloud-infrastructure-engineering.ansible.state-parameter-semantics-present-absent-latest
name: state-parameter-semantics-present-absent-latest
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, modules-fqcn, state-parameter, state-latest, idempotency, package-module]
level: intro
status: docs-checked
description: "Understand the state parameter across modules: present, absent, latest, started, restarted, directory, touch, and which states are idempotent or always change."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/file.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/dnf.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/apt.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/package.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/service.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/user.py", "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/mount.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The state parameter

Most modules are declarative: `state` describes the end result, the module computes whether to change.

| Module family | States | Notes |
|---|---|---|
| packages (dnf, apt, package) | `present`/`installed`, `absent`/`removed`, `latest` (apt also `build-dep`, `fixed`) | `latest` installs a newer version whenever one appears, so runs are not reproducible; `package` supports only the states the underlying module supports |
| service/systemd_service | `started`, `stopped`, `restarted`, `reloaded` | `started`/`stopped` are idempotent; `restarted` always bounces the unit and `reloaded` always reloads, so put them in handlers |
| file | `file`, `directory`, `link`, `hard`, `touch`, `absent` | `touch` updates access and modification times, so it always reports changed (module docs) |
| user/group | `present`, `absent` | on `user`, `state: absent` with `remove: true` attempts to remove the user's directories |
| lineinfile/blockinfile | `present`, `absent` | |
| mount (ansible.posix) | `mounted`, `unmounted`, `present`, `absent`, `remounted`, `ephemeral` (also `absent_from_fstab`, `absent_keep_mountpoint`) | `present` configures fstab only; `mounted` mounts and configures fstab; `ephemeral` ignores fstab |

## Patterns
```yaml
- ansible.builtin.dnf:
    name: [nginx-1.24.0, openssl]
    state: present                     # a version in the name pins it (dnf accepts name-1.0 style specifiers)
- ansible.builtin.service:
    name: nginx
    state: started
    enabled: true                      # enabled is separate from state
```

## Gotchas
- Defaults differ per module: for `file`, an unspecified `state` means the current state of the path is assumed to be the desired state, and `state: file` expects the path to be a file.
- `state: latest` makes reruns change things whenever a newer version is published; reserve it for patch playbooks.
- For services, `enabled` (start on boot) and `state` (current state) are separate; at least one is required.

## Verify
- [ ] A second run reports `changed=0` (except intentional restarts).

## Checked
Checked 2026-10-26 against ansible-core devel `file.py`, `dnf.py`, `apt.py`, `package.py`, `service.py`, `systemd_service.py`,
`user.py` and ansible.posix `mount.py` documentation blocks. Confirmed the state choices in the table, restart/reload
semantics, `touch` always changed, `mount` state meanings, `user` `remove`. Removed the unconfirmed cloud-resources row and the
claim that `state: file` fails on a missing path.
Method: documentation only; no commands were run.
