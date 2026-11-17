---
id: computing-software.cloud-infrastructure-engineering.ansible.services-and-systemd-units
name: services-and-systemd-units
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, services, systemd, service-module, systemd-service, systemd-units, unit-files, drop-in, daemon-reload, service-facts, enabled, masked, timers, systemd-timer, user-services, scope-user, restart-handlers, reload-vs-restart, socket-activation, wait-for]
level: practitioner
status: docs-checked
description: "Manage services with Ansible: systemd vs service module, unit files and drop-ins with daemon_reload, enable/mask/timers, user-scope units, service_facts checks, and reload-vs-restart handlers."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/systemd_service_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/systemd_service.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/service.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/service_facts.py", "https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml", "https://github.com/systemd/systemd/blob/main/man/systemd.timer.xml", "https://github.com/systemd/systemd/blob/main/man/systemctl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Services and systemd units

**Goal:** services that are enabled, running the config Ansible wrote, restarted
only when needed, and whose unit files are managed as code.

## 1. State and enablement
```yaml
- ansible.builtin.systemd_service:        # alias: systemd; use service for non-systemd (sysvinit, BSD, OpenRC)
    name: nginx
    state: started          # started | stopped | restarted | reloaded
    enabled: true
    masked: false
```
`enabled` means the unit starts on boot, and `state` is the current state; at least one is required.
`masked: true` makes the unit impossible to start. `ansible.builtin.service` is the generic module: it uses the
`ansible_service_mgr` fact to pick a backend (`use` forces one) and has no `masked`, `daemon_reload` or `scope`.
`started`/`stopped` are idempotent, while `restarted` always bounces the unit and `reloaded` always reloads.

## 2. Unit files and drop-ins
```yaml
- ansible.builtin.template:
    src: app.service.j2
    dest: /etc/systemd/system/app.service
    mode: "0644"
  notify: [daemon reload, restart app]
- ansible.builtin.file: {path: /etc/systemd/system/nginx.service.d, state: directory}
- ansible.builtin.copy:
    dest: /etc/systemd/system/nginx.service.d/limits.conf
    content: |
      [Service]
      LimitNOFILE=65536
  notify: [daemon reload, restart nginx]
handlers:
  - name: daemon reload
    ansible.builtin.systemd_service: {daemon_reload: true}
  - name: restart app
    ansible.builtin.systemd_service: {name: app, state: restarted}
```
Handlers run in the order they are **defined**, so define `daemon reload` first. Or set
`daemon_reload: true` directly on the restart task: the module runs `daemon-reload` before any other operation.
A drop-in directory `foo.service.d/` holds `.conf` files that change settings without modifying the unit file (systemd.unit).
Prefer an `ExecReload=` setting plus `state: reloaded` for daemons that support reloading.

## 3. Timers instead of cron
```yaml
# backup.timer + backup.service deployed with template, then:
- ansible.builtin.systemd_service: {name: backup.timer, state: started, enabled: true, daemon_reload: true}
```
Timers support `Persistent=true` catch-up and `RandomizedDelaySec=` (systemd.timer). Template both the `.timer` and
the `.service` file.

## 4. User-scope services
```yaml
- ansible.builtin.systemd_service: {name: podman-app, state: started, enabled: true, scope: user}
  become: true
  become_user: app
```
For `scope: user` the executing user needs its own dbus instance, normally via the `XDG_RUNTIME_DIR` variable; the module
documentation warns of `Failed to connect to bus: no such file or directory` otherwise and shows an `environment` example.

## 5. Checking rather than acting
```yaml
- ansible.builtin.service_facts:
- ansible.builtin.assert:
    that: ansible_facts.services['sshd.service'].state == 'running'
- ansible.builtin.wait_for: {port: 5432, host: 127.0.0.1, timeout: 60}   # readiness after a restart
```
`service_facts` keys include the `.service` suffix on systemd hosts (the module's examples use `ntpd.service`).

## Gotchas
- `state: restarted` on every run (no handler, no `when`) is the classic non-idempotent play; always restart via a handler or `when: cfg is changed`.
- A handler notified by several tasks still runs once, at the end of the play; a failed task later means it never runs unless `force_handlers: true` (play) or `--force-handlers`.
- Unit files with no `[Install]` section are reported as `static` by systemctl ("no provisions for enabling"), so `enabled` does not apply to them.
- `systemd_service` is for systemd hosts; for other init systems use `ansible.builtin.service`.

## Verify
- [ ] Second run: `changed=0`, no restarts; editing the template triggers exactly one reload/restart.
- [ ] `systemctl is-enabled`/`is-active` match the play for each managed unit, including timers.

## Checked
Checked 2026-10-26 against ansible-core devel `systemd_service.py`, `service.py`, `service_facts.py` and systemd
`man/systemd.unit.xml`, `systemd.timer.xml`, `systemctl.xml`. Confirmed: `enabled`/`state`/`masked`/`daemon_reload`/`scope`
options, restart/reload semantics, `service` fallback via `ansible_service_mgr` and `use`, `.service` key suffix in
`service_facts`, drop-in directories, `Persistent=`/`RandomizedDelaySec=`, `static` units, the user-scope dbus and
`XDG_RUNTIME_DIR` note. Removed unconfirmed claims: `loginctl enable-linger`, `firewalld`/`nftables` masking example,
`NeedDaemonReload`, systemd warning behaviour, `[Install]` failure text, container and Alpine/FreeBSD remarks.
Method: documentation only; no commands were run.
