---
id: computing-software.cloud-infrastructure-engineering.ansible.pre-merge-validation-chain-preflight-asserts-and-check-mode-gaps
name: pre-merge-validation-chain-preflight-asserts-and-check-mode-gaps
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, syntax-check-dry-run, validation-chain, preflight-checks, check-mode-unsupported, check-mode]
level: practitioner
status: docs-checked
description: "Order pre-merge validation (syntax-check, ansible-lint, check mode), add preflight assert plays, and handle tasks that report nothing in check mode."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/assert_module.html", "https://ansible.readthedocs.io/projects/lint/usage/", "https://ansible.readthedocs.io/projects/lint/profiles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Validation chain, preflight asserts and check-mode gaps

## Order (cheap and fast first)
1. `ansible-playbook playbooks/site.yml --syntax-check` — parse, imports resolve.
2. `ansible-lint --profile=production` — rule profiles from `min` through `production`;
   `production` is the strictest and ensures content meets requirements for inclusion in
   Ansible Automation Platform. ansible-lint itself runs `ansible-playbook --syntax-check` on
   playbooks and roles, so write roles that parse without variables supplied.
3. `ansible-playbook site.yml --check --diff --limit <canary-host>` — against a real staging
   host. Diff mode makes a lot of output, so check one host at a time.
Fail fast: stop at the first failing stage so feedback is quick.

## Preflight assert play
```yaml
- name: Preflight
  hosts: all
  any_errors_fatal: true
  tasks:
    - ansible.builtin.assert:
        that:
          - app_release is defined
        fail_msg: "Preflight failed on {{ inventory_hostname }}"
        quiet: true
```
`ansible.builtin.assert` takes `that`, `fail_msg` (called `msg` before Ansible 2.7, still an
alias), `success_msg` and `quiet`. Import the play first in site.yml; `any_errors_fatal`
stops the run for all hosts when one host fails.

## Tasks that report nothing in check mode
In check mode, modules that support it report the changes they would make; modules that do
not support check mode report nothing and do nothing. Check mode is a simulation and does
not produce output for tasks whose conditionals depend on registered variables from prior
tasks. Consequences and fixes:
- A later task depending on the skipped task's register fails or behaves differently.
- Set `check_mode: false` on read-only tasks (they then run for real even with `--check`)
  and guard dependants:
```yaml
- ansible.builtin.command: app --version
  register: ver
  check_mode: false
  changed_when: false
- ansible.builtin.debug: {msg: "{{ ver.stdout }}"}
  when: not ansible_check_mode
```
- `ansible_check_mode` is a magic variable, True when running in check mode; use
  `when: not ansible_check_mode` to skip a task, or `ignore_errors: "{{ ansible_check_mode }}"`.
- A module's documentation has an Attributes section stating its check mode support.

## Verify
- [ ] `--check` run on staging completes with no failures caused by skipped prerequisites.

## Checked
2026-11-09. Confirmed in the Ansible check mode and diff mode page (behaviour of modules
without check mode support, check_mode true/false, ansible_check_mode, diff output size),
the assert module documentation (parameters, msg alias), and ansible-lint usage and profile
pages (--profile, production profile purpose, syntax-check run). Removed as unconfirmed:
yamllint and Molecule stages, the inventory parse step, `command`/`shell` skip rules with
creates/removes, the ansible-doc attributes command, the fact-based and regex assertions in
the example, and the size-available assertion.
Method: documentation only; no commands were run.
