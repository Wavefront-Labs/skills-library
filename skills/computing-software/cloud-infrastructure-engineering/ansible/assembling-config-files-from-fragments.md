---
id: computing-software.cloud-infrastructure-engineering.ansible.assembling-config-files-from-fragments
name: assembling-config-files-from-fragments
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, files-archives, assemble, fragments, conf-d, validate]
level: practitioner
status: docs-checked
description: "Build one config file from fragments contributed by several roles with ansible.builtin.assemble, ordering by filename, validating the result, and cleaning stale fragments."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/assemble_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/blockinfile_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/assemble.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assembling config files from fragments

Use when several roles must contribute to one file for a program that takes a single configuration
file and has no `conf.d`-style include directory (this is the case the module is documented for).

```yaml
# role A
- ansible.builtin.copy:
    dest: /etc/app/fragments/10-base.conf
    content: "{{ lookup('template', 'base.conf.j2') }}"
    mode: "0644"
  notify: Assemble app config

# role B
- ansible.builtin.copy:
    dest: /etc/app/fragments/50-plugin-x.conf
    content: "plugin x enabled\n"
  notify: Assemble app config

handlers:
  - name: Assemble app config
    ansible.builtin.assemble:
      src: /etc/app/fragments
      dest: /etc/app/app.conf
      regexp: '\.conf$'          # only these files
      delimiter: "\n# ---\n"     # optional separator between fragments
      validate: /usr/bin/app --check-config %s
      mode: "0644"
      backup: true
    notify: Restart app
```
Fragments are concatenated in **string sort order** of filenames — use numeric prefixes with
fixed width (`10-`, `50-`, `90-`).

`remote_src` defaults to `true` (fragments are read on the target, as in the example above).
With `remote_src: false`, `src` is searched for on the controller instead, so the fragments do not
need to exist on the host. `regexp` uses Python regular expressions, and the `validate` command is run
without a shell (no expansion or pipes).

## Stale fragments
If a role is removed, its fragment stays. Either manage the directory exhaustively (find + remove
unknown files) or have each role remove its fragment when disabled (`state: absent`).

## Alternatives
- A native include directory in the program itself, when it has one.
- `blockinfile` with distinct `marker`s per role in one file — fine for 2–3 contributors.
- A single template with a merged data structure (`role_a_items + role_b_items`) — best when all data is in Ansible.

## Gotchas
- The module compares the SHA-1 of the assembled result with `dest` and only writes (and validates) when they differ.
- `ignore_hidden: true` skips files whose names start with `.` (default `false`).
- `validate` runs before copying into place; `%s` (the path to check) must be present or the module fails.

## Verify
- [ ] `--check --diff` after a second run: no change to app.conf.
- [ ] Validate command passes on the assembled file.

## Checked
Checked 2026-10-26 against ansible-core devel `lib/ansible/modules/assemble.py` (documentation block and code; repository
last commit 2026-10-23). Confirmed: string sort order, `src`/`dest`/`regexp`/`delimiter`/`validate`/`backup`/
`ignore_hidden`/`remote_src` names, `remote_src` default true, `%s` required, checksum comparison. Removed unconfirmed
claims about sudoers, HAProxy, authorized_keys and crontab use cases and specific include directories.
Method: documentation only; no commands were run.
