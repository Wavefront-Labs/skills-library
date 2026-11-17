---
id: computing-software.cloud-infrastructure-engineering.ansible.guarding-against-accidental-hosts-all-runs
name: guarding-against-accidental-hosts-all-runs
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, playbook-syntax, hosts-all-guard, limit, prod-safeguards]
level: practitioner
status: docs-checked
description: "Prevent playbooks from running against every host by accident: safe defaults for hosts, required limits, assert guards and confirmation for production."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Guarding against accidental hosts: all runs

## 1. Never default to all
```yaml
- hosts: "{{ target | default('nobody') }}"
```
A missing `-e target=` then matches no host (the run only warns that the host pattern did not match, per `host_pattern_mismatch`, default `warning`) instead of targeting the estate.

## 2. Require --limit
```yaml
- hosts: all
  gather_facts: false
  tasks:
    - name: Refuse to run without --limit
      ansible.builtin.assert:
        that: (ansible_limit | default('', true)) | length > 0
        fail_msg: "Run with --limit; this playbook must not target the whole inventory"
      run_once: true
      delegate_to: localhost
```
`ansible_limit` holds the contents of the `--limit` option; the expression above also fails when it is undefined or empty.

## 3. Cap the blast radius
```yaml
- hosts: web
  serial: 5
  max_fail_percentage: 0
  pre_tasks:
    - ansible.builtin.assert:
        that: ansible_play_hosts_all | length <= 50
        fail_msg: "{{ ansible_play_hosts_all | length }} hosts targeted; max 50 per run"
      run_once: true
```

## 4. Human confirmation for production
```yaml
    - ansible.builtin.pause:
        prompt: "Type the environment name ({{ env }}) to continue"
      register: confirm
      run_once: true
      when: env == 'prod' and not (ci | default(false) | bool)
    - ansible.builtin.assert:
        that: confirm.user_input == env
      run_once: true
      when: confirm is not skipped
```

## 5. Default inventory to non-prod
`inventory = inventories/staging` in ansible.cfg; production requires an explicit `-i inventories/prod` (command-line `-i` overrides the config setting).

## Gotchas
- `--list-hosts` before every manual production run; make it a habit or a wrapper script. It lists the hosts each play targets without running tasks, so the `assert` guards above do not fire in that mode.
- `pause` returns `user_input` only when no `seconds` or `minutes` is set, and with `serial` it prompts once per batch; `echo: false` hides typed input. The `ci` variable in the example is yours to define for unattended runs.

## Verify
```bash
ansible-playbook site.yml --list-hosts                 # with guard 1 and no -e target=, lists no hosts for the play
```

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) reference_appendices/special_variables.rst (`ansible_limit`, `ansible_play_hosts_all`), playbook_guide/playbooks_strategies.rst (`serial`), general_precedence.rst, and ansible-core `config/base.yml` (HOST_PATTERN_MISMATCH default warning). Confirmed: magic variable meanings, host-pattern-mismatch behaviour, command-line inventory override. Rewrote the `--limit` guard so it does not depend on whether `ansible_limit` is undefined or empty without `--limit` (not documented), and corrected the verify step, since `--list-hosts` does not run assert tasks. Removed the unconfirmed claim about the variable's introduction version and the controller advice.
Method: documentation only; no commands were run.
