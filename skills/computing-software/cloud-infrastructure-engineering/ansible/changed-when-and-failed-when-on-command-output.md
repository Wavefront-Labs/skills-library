---
id: computing-software.cloud-infrastructure-engineering.ansible.changed-when-and-failed-when-on-command-output
name: changed-when-and-failed-when-on-command-output
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, idempotency, changed-when-stdout, changed-when-false, failed-when, no-changed-when]
level: practitioner
status: docs-checked
description: "Make command and shell tasks report honest status with changed_when on stdout, rc or a before/after compare, changed_when false for reads, and failed_when for odd exit codes."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/command_module.html", "https://github.com/ansible/ansible-lint/blob/main/docs/rules/no-changed-when.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# changed_when and failed_when on command output

`command` and `shell` run arbitrary commands, so Ansible cannot tell whether they changed anything
unless you say so with `changed_when`, `creates` or `removes` (the ansible-lint rule
`no-changed-when` flags tasks that do neither). A false "changed" triggers handlers and hides real drift.

## Read-only commands
```yaml
- name: Get current schema version
  ansible.builtin.command: /opt/app/bin/schema-version
  register: schema
  changed_when: false
  check_mode: false     # run even in --check so later tasks have data
```

## Changed when the tool says so
```yaml
- name: Run migrations
  ansible.builtin.command: /opt/app/bin/migrate
  register: mig
  changed_when: "'No migrations to apply' not in mig.stdout"

- name: Enable apache module
  ansible.builtin.command: a2enmod rewrite
  register: a2
  changed_when: "'already enabled' not in a2.stdout"
  notify: Restart apache
```
Return codes can define both results:
```yaml
- ansible.builtin.command: /opt/app/bin/check-state
  register: cs
  changed_when: cs.rc == 2
  failed_when: cs.rc not in [0, 2]
```

## Compare before and after
When output is not informative:
```yaml
- ansible.builtin.command: sysctl -n net.core.somaxconn
  register: before
  changed_when: false
- ansible.builtin.command: sysctl -w net.core.somaxconn=4096
  changed_when: true
  when: before.stdout | int != 4096
```
(Prefer a real module such as `ansible.posix.sysctl` whenever one exists.)

## Combining conditions
Lists are joined with an implicit `and`: the task fails (or changes) only when all conditions are
met. To act when any condition is met, use one string with an explicit `or`:
```yaml
failed_when:
  - r.rc != 0
  - "'already exists' not in r.stderr"
changed_when: "r.rc == 0 or 'created' in r.stdout"
```
`_task.result` gives access to the task's result without `register` (usable in `when`, `until`,
`failed_when`, `changed_when`, `break_when`).

## Gotchas
- `changed_when` and `failed_when` are raw Jinja2 expressions; do not wrap them in `{{ }}` (Ansible warns).
- `command` only supports check mode through `creates`/`removes` (check mode support is "partial"), so
  conditions that read `r.stdout` in later tasks need `check_mode: false` on the read-only probe.
- `failed_when: false` hides genuine failures; narrow it to known return codes.
- A successful exit code that is not zero can also be handled with `shell: cmd || /bin/true`.

## Verify
- [ ] A second consecutive run reports `changed=0` for these tasks.
- [ ] ansible-lint `no-changed-when` is clean.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_error_handling.rst), ansible-core devel
`modules/command.py` (check mode "partial", `creates`/`removes`) and the ansible-lint `no-changed-when` rule
page. Confirmed list-is-`and` semantics, `_task.result`, raw-expression warning. Removed unconfirmed claims:
the `needs-restarting` exit code, locale (`LC_ALL`) advice, and "command always reports changed" (reworded).
Method: documentation only; no commands were run.
