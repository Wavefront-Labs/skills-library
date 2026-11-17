---
id: computing-software.cloud-infrastructure-engineering.ansible.syntax-check-check-mode-and-dry-run-validation
name: syntax-check-check-mode-and-dry-run-validation
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, syntax-check, dry-run, validation, check-mode, diff-mode, ansible-playbook-check, list-tasks, list-hosts, check-mode-false, ansible-check-mode, assert, validate-argument-spec, yamllint, pre-flight, canary-run, limit, change-preview]
level: practitioner
status: docs-checked
description: "Validate an Ansible change before prod: lint, --syntax-check, --list-hosts/--list-tasks, --check --diff on a canary, check_mode-aware tasks, argument specs and asserts."
sources: ["Validating tasks: check mode and diff mode (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html)", "Roles, role argument validation (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-argument-validation)", "Getting started with playbooks, verifying playbooks (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)", "ansible-playbook CLI option source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/playbook.py)", "ansible-lint profiles (https://github.com/ansible/ansible-lint/blob/main/docs/profiles.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Syntax check, check mode and dry-run validation

**Goal:** a layered pre-flight that catches typos, wrong targets and unintended
changes before any real run, and a dry run that is actually trustworthy.

## 1. The ladder (cheap to expensive)
```bash
yamllint -c .yamllint .                                   # indentation, duplicates, truthy
ansible-lint --profile production                          # keywords, FQCN, idempotency smells
ansible-playbook site.yml --syntax-check                   # syntax check only; nothing is executed
ansible-playbook site.yml --list-hosts --list-tasks --list-tags -l web   # the blast radius and plan
ansible-playbook site.yml --check --diff -l web-canary-01  # dry run on one host
ansible-playbook site.yml --diff -l web-canary-01          # real run on one host
ansible-playbook site.yml --diff                           # fleet, with serial in the play
```
`--syntax-check` performs a syntax check on the playbook without executing it, so follow it with `--check`.
`--list-hosts` with the real `-l`/inventory is the last step before any destructive play:
it is a cheap way to confirm a pattern like `web:&prod:!canary`.

## 2. Make check mode honest
`--check` runs without changing remote systems: modules that support check mode report the changes they would have made; modules that do not support it report nothing and do nothing. Check mode will not produce output for tasks whose conditionals depend on registered results of earlier tasks. Problems and fixes:
```yaml
- ansible.builtin.command: /opt/app/bin/version        # skipped under --check -> later vars undefined
  register: ver
  check_mode: false                                     # always run (read-only command)
  changed_when: false
- ansible.builtin.template: {src: app.conf.j2, dest: /etc/app.conf}
  check_mode: false                                     # run for real even under --check (rare; use only for harmless changes)
- ansible.builtin.set_fact: {port: "{{ ver.stdout | int + 1 }}"}   # now works in --check
- ansible.builtin.service: {name: app, state: restarted}
  when: not ansible_check_mode                          # avoid misleading "changed" in check runs
```
Rules: every read-only `command`/`shell` gets `check_mode: false` + `changed_when: false`;
anything whose result feeds later tasks must run in check mode or the dry run dies with
"undefined variable" halfway and tells you nothing about the rest. Custom modules: declare
`supports_check_mode=True` and branch on `module.check_mode`.

`--diff` adds before/after for files, templates, `lineinfile`, users, and modules that
return `diff`; `--check --diff` together is the review artefact to paste into a change ticket.
`ansible_check_mode` and `ansible_diff_mode` are available as variables.

## 3. Pre-flight assertions in the play
```yaml
- hosts: db
  pre_tasks:
    - ansible.builtin.assert:
        that:
          - ansible_facts.distribution_major_version | int >= 9
          - pg_version is defined and pg_version is version('14', '>=')
          - inventory_hostname in groups['db']
        fail_msg: "Pre-flight failed on {{ inventory_hostname }}"
        quiet: true
      run_once: false
```
Roles with a `meta/argument_specs.yml` (or `.yaml`) file get a validation task inserted at the beginning of role execution; if the parameters fail the specification the role fails before its tasks run (available since ansible-core 2.11) — write the spec for every role you ship.

## 4. Canary and staged rollout
Combine: `-l canary` first, `serial: [1, "10%", "100%"]` in the play, `max_fail_percentage`,
and a post-task health check (`uri` with `until`). A `--check` that reports zero changes on a
host that *should* change means your conditionals are wrong, not that it is safe.

## Gotchas
- `--diff` can reveal sensitive information; set `diff: false` on tasks that handle secrets.
- To gate CI on "no unexpected changes", parse the play recap (`changed=`) rather than relying on the exit code.
- Running single tasks with `check_mode: true` is a way to test the conditions under which a module would make changes.

## Verify
- [ ] `--syntax-check`, `--list-tasks` and `--check --diff -l canary` all complete without errors on the branch before merge.
- [ ] A `--check` run on a converged host reports `changed=0` (no read-only commands masquerading as changes).
- [ ] A missing required role variable fails via `argument_specs` with a message naming the variable.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21), ansible-core 2.21.5 and ansible-lint docs.
- Confirmed: `--syntax-check`, `--list-hosts`, `--list-tasks`, `--list-tags`, `--check`, `--diff`; `check_mode: false` and `check_mode: true` task options; `ansible_check_mode`; modules without check-mode support do nothing; `diff: false`; role argument validation inserted at the start of a role (since 2.11); ansible-lint profiles min, basic, moderate, safety, shared, production.
- Removed as unconfirmed: statements about static versus dynamic includes under `--syntax-check`, package-cache behaviour in check mode, handler behaviour in check mode, and the exit-code remark.
- Removed a `validate_argument_spec` pre-task that referenced `role_path`, which is not defined in a play's `pre_tasks`.

Method: documentation only; no commands were run.
