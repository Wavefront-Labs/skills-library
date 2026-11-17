---
id: computing-software.cloud-infrastructure-engineering.ansible.verifying-unit-files-with-systemd-analyze
name: verifying-unit-files-with-systemd-analyze
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, services-systemd, systemd-analyze, validate, unit-files]
level: practitioner
status: docs-checked
description: "Validate templated systemd unit files with systemd-analyze verify via the template validate option, and audit service hardening with systemd-analyze security."
sources: ["https://www.freedesktop.org/software/systemd/man/latest/systemd-analyze.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Verifying unit files with systemd-analyze

## Validate before installing
```yaml
- name: Install app unit (validated)
  ansible.builtin.template:
    src: app.service.j2
    dest: /etc/systemd/system/app.service
    mode: "0644"
    validate: /usr/bin/systemd-analyze verify %s
  notify: Restart app
```
`validate` runs the command against a temporary file path passed through `%s` before the file is copied to the destination; `%s` must be present, and the command is not run through a shell (no pipes or expansion).

`systemd-analyze verify` loads the given file and also the units it references, using the directories of the command-line arguments plus the usual unit load paths. A unit's name on disk can be overridden with an alias after a colon (`systemd-analyze verify /tmp/source:alias.service`), which is the way to give a temporary file the unit name it should have. If the temporary file name causes false failures, render to a staging path instead, verify, then copy:
```yaml
- ansible.builtin.template:
    src: app.service.j2
    dest: /etc/systemd/system/.staging/app.service
    mode: "0644"
  register: staged
- ansible.builtin.command: systemd-analyze verify /etc/systemd/system/.staging/app.service
  changed_when: false
  when: staged is changed
- ansible.builtin.copy:
    src: /etc/systemd/system/.staging/app.service
    dest: /etc/systemd/system/app.service
    remote_src: true
    mode: "0644"
  notify: Restart app
```
Documented detections: unknown sections and directives, missing dependencies required to start the unit, man pages in `Documentation=` not found, and commands in `ExecStart=` and similar that are not found or not executable.

## Hardening audit
```bash
systemd-analyze security app.service --no-pager        # overall exposure level and per-setting table
```
Assert a maximum exposure in CI or a check play:
```yaml
- ansible.builtin.command: systemd-analyze security app.service --threshold=5
  changed_when: false
```
With `--threshold=NUMBER`, `security` returns an error if the unit's overall exposure level is greater than the number (the default threshold is 100).

## Other subcommands
`systemd-analyze blame` (time per unit at boot), `critical-chain [UNIT...]`, `calendar` (parses and normalizes `OnCalendar=` expressions and shows when they elapse next), `timespan` (parses time spans).

## Verify
- [ ] A deliberately broken directive makes the play fail before the unit is replaced.

## Checked
2026-11-01. Confirmed against the systemd-analyze manual (verify detections, alias after a colon, referenced units, `security`, `--threshold` and its default of 100, `blame`, `critical-chain`, `calendar`, `timespan`) and the ansible.builtin.template page (`validate` with `%s`, no shell features). Removed: the claim that verify needs a `.service` suffix and that a temp name fails, the 0-10 score range, the systemd 250+ version gate, and the absolute-path wording.
Method: documentation only; no commands were run.
