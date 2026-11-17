---
id: computing-software.cloud-infrastructure-engineering.ansible.resetting-connections-with-meta-reset-connection
name: resetting-connections-with-meta-reset-connection
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, connection-plugins, reset-connection, meta, controlpersist]
level: practitioner
status: docs-checked
description: "Use meta reset_connection to drop persistent SSH sessions so group membership, environment or login shell changes take effect mid-play."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/meta_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/ssh_connection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# meta: reset_connection

`meta: reset_connection` interrupts a persistent connection (for example ssh with ControlPersist; the ssh plugin's default `ssh_args` include `ControlMaster=auto` and `ControlPersist=60s`). A login session's group list is fixed at login, so a change such as a new group membership is not visible to later tasks until the connection is re-established; the module's own example resets the connection "to allow user changes to affect the current login user".

## Classic case: add user to docker group
```yaml
- name: Add automation user to docker group
  ansible.builtin.user:
    name: "{{ ansible_user }}"
    groups: docker
    append: true

- name: Drop the persistent connection so new group membership applies
  ansible.builtin.meta: reset_connection

- name: Now works without sudo
  ansible.builtin.command: docker ps
  changed_when: false
```

## Other triggers
- Any change to the login user that only applies to new logins (group membership is the documented example).
- After changing connection variables such as `ansible_user` or `ansible_port` via `set_fact` mid-play, so the next task reconnects with them.

## Behaviour
- `reset_connection` is added in Ansible 2.3; per the `meta` module notes it does not itself connect to the remote host.
- Only some `meta` options support conditionals, and those that do act by bypassing the host loop and taking values from the first available host; `delegation` is not supported.

## Gotchas
- If you change the port or user the next connection must use, update `ansible_port` or `ansible_user` (for example with `set_fact`) before the reset so the reconnect targets the new values.

## Verify
```yaml
- ansible.builtin.command: id -nG
  register: g
  changed_when: false
- ansible.builtin.assert:
    that: "'docker' in g.stdout.split()"
```

## Checked
Checked 2026-10-25 against the ansible-core devel `meta` module documentation (reset_connection, version_added 2.3, example text, attribute notes) and the ssh connection plugin source (default `ssh_args` with ControlMaster and ControlPersist=60s). Confirmed: purpose and example of `reset_connection`, version, conditional and delegation limits of `meta`. Removed unconfirmed claims about network_cli, paramiko and local behaviour, `/etc/environment`, PAM limits and `~/.ssh/config` multiplexing; the group-membership example is kept as the documented use case.
Method: documentation only; no commands were run.
