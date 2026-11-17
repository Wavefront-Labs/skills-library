---
id: computing-software.cloud-infrastructure-engineering.ansible.systemd-unit-environment-and-resource-limits
name: systemd-unit-environment-and-resource-limits
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, services-systemd, unit-environment, systemd-env, drop-in, limitnofile, environmentfile]
level: practitioner
status: docs-checked
description: "Set environment variables and resource limits for services through systemd drop-ins and EnvironmentFile from Ansible, with daemon_reload and restart only on change."
sources:
  - "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/systemd_service.py"
  - "https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml"
  - "https://github.com/systemd/systemd/blob/main/man/systemd.resource-control.xml"
  - "https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd unit environment and resource limits

Do not edit vendor units; add a drop-in in a `<unit>.d/` directory under `/etc/systemd/system/`. The systemd.unit man page says all `.conf` files in the `.d/` subdirectory are read, and drop-ins with different names are applied in lexicographic order.

```yaml
- name: Drop-in directory
  ansible.builtin.file:
    path: /etc/systemd/system/app.service.d
    state: directory
    mode: "0755"

- name: Limits and environment drop-in
  ansible.builtin.copy:
    dest: /etc/systemd/system/app.service.d/10-ansible.conf
    mode: "0644"
    content: |
      [Service]
      Environment="JAVA_OPTS=-Xmx{{ app_heap_mb }}m" "TZ=UTC"
      EnvironmentFile=-/etc/app/app.env
      LimitNOFILE=65536
      MemoryMax={{ app_memory_max }}
      CPUQuota=200%
      TasksMax=4096
  notify: Restart app

- name: Environment file
  ansible.builtin.template:
    src: app.env.j2
    dest: /etc/app/app.env
    mode: "0600"
    owner: root
  notify: Restart app

handlers:
  - name: Restart app
    ansible.builtin.systemd_service:
      name: app
      state: restarted
      daemon_reload: true      # re-read unit files after changing them
```

## Notes
- `EnvironmentFile=`: a missing, unreadable or invalid file makes the service fail to start; prefix the path with `-` to make the file optional (all errors about it are silently ignored). Variables from these files override `Environment=`. Shell variables such as `$HOME` are not expanded in the path; use `%h`-style specifiers.
- File format: newline-separated assignments; empty lines and lines starting with `;` or `#` are ignored. Values follow POSIX-shell-like quoting rules, but it is not a shell script.
- `Environment=`: put quotes around a whole assignment containing spaces; `$` has no special meaning and variables are not expanded. Assigning an empty string resets the list. A later setting of the same variable overrides an earlier one.
- Secrets: the systemd.exec page says environment variables are not suitable for passing secrets (they are exposed to unprivileged clients over D-Bus and propagate to child processes) and recommends `LoadCredential=`, `LoadCredentialEncrypted=` or `SetCredentialEncrypted=` instead. An EnvironmentFile is still environment, so prefer credentials for secrets.
- `LimitNOFILE=` is the unit equivalent of `ulimit -n`; the other `Limit*=` directives map to the other ulimit options.
- `MemoryMax=` takes bytes with K, M, G, T suffixes (base 1024) or a percentage of physical memory, `infinity` for no limit, and controls `memory.max`; the docs recommend `MemoryHigh=` as the main control and `MemoryMax=` as the last line of defence. `CPUQuota=` takes a percentage of one CPU, and values above 100% allow more than one CPU. An empty value unsets it.
- User units: `scope: user` on `systemd_service` (choices are `system`, `user`, `global`; added in Ansible 2.7).

## Gotchas
- `daemon_reload: true` is how the module reloads systemd after unit files change; without it the manager keeps the old definition.
- Drop-in names sort lexically; the later file wins for settings that take a single value.

## Verify
- [ ] `systemctl show app -p LimitNOFILE -p MemoryMax -p Environment` reflects the values.

## Checked

2026-11-09. Checked against the ansible.builtin.systemd_service module source (`daemon_reload`, `scope` choices, `state` choices) and the systemd man pages systemd.exec, systemd.resource-control and systemd.unit (drop-in handling, `Environment=`, `EnvironmentFile=` and its `-` prefix, `LimitNOFILE=`, `MemoryMax=`, `CPUQuota=`, `TasksMax=`).

Corrected: secrets were advised to go into a 0600 EnvironmentFile; the man page advises credentials instead. Removed as unsupported by those pages: the `limits.conf` statement, the cgroup v2 and `MemoryLimit` note and OS versions, the `ExecStart=` clearing example, the "systemctl status warns" remark and the `/proc` limits check.

Method: documentation only; no commands were run.
