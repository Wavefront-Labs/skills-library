---
id: computing-software.cloud-infrastructure-engineering.ansible.reading-module-return-values-with-register
name: reading-module-return-values-with-register
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, modules-fqcn, return-values, stdout-lines, register, common-return-values]
level: practitioner
status: docs-checked
description: "Register module results and use the common return values (changed, failed, rc, stdout, stdout_lines, stderr, msg, results) plus module-specific keys found via ansible-doc."
sources: ["Return values (https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html)", "Using variables, registering variables (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)", "Loops, using register in a loop (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)", "Tests, task results (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tests.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading module return values

```yaml
- name: Check service status
  ansible.builtin.command: systemctl is-active nginx
  register: nginx_state
  changed_when: false
  failed_when: nginx_state.rc not in [0, 3]

- ansible.builtin.debug:
    var: nginx_state
```
Always `debug: var=<registered>` once while developing — the exact keys differ by module.

## Common return values
| Key | Present | Notes |
|---|---|---|
| `changed` | all | bool |
| `failed` | all | bool; test with `is failed` |
| `skipped` | when skipped | registered var still exists, with `skipped: true` |
| `msg` | most | human message, errors |
| `rc` | command-like | exit code |
| `stdout`, `stderr` | command-like | strings |
| `stdout_lines`, `stderr_lines` | command-like | lists split on newlines |
| `results` | loops | list of per-item results, each with `item` |
| `invocation` | most modules | module args as received |
| `diff` | diff-capable modules | before/after |
| `backup_file` | file modules with `backup: true` | path |
| `warnings`, `deprecations`, `exception` | any | `exception` holds traceback information and is only displayed at high verbosity (`-vvv`) |

Module-specific keys are documented in the RETURN section: `ansible-doc ansible.builtin.stat`
→ `stat.exists`, `stat.mode`, `stat.checksum`...

## Using them
```yaml
- ansible.builtin.stat: {path: /etc/app.conf}
  register: conf
- ansible.builtin.template: {src: app.conf.j2, dest: /etc/app.conf}
  when: not conf.stat.exists

- ansible.builtin.debug:
    msg: "{{ item }}"
  loop: "{{ nginx_state.stdout_lines }}"
```
Status tests are more robust than key checks: `when: result is changed / is failed / is succeeded / is skipped`.

## Registered variables in loops
`register` on a loop gives a structure with a `results` list (one entry per item, each with `item`) and `msg: All items completed`:
```yaml
- ansible.builtin.command: "id {{ item }}"
  loop: [alice, bob]
  register: ids
  failed_when: false
- ansible.builtin.debug:
    msg: "{{ item.item }} rc={{ item.rc }}"
  loop: "{{ ids.results }}"
  when: item.rc != 0
```

## Gotchas
- A failed or skipped task still registers a variable (with `failed` or `skipped: true` and no `stdout`), unless it was skipped by tags. Guard with `when: r is not skipped` or use different names.
- Registered variables are host-level, kept in memory, and valid for the rest of the playbook run including later plays; they cannot be cached for future runs. From another host use `hostvars['h1'].nginx_state`.
- New in ansible-core 2.21: `register` also accepts a dictionary of `variable: expression` pairs evaluated after the task, using the implicit `_task.result` (for example `register: {rc_only: _task.result.rc}`). Write the expressions without `{{ }}`, and do not use `_task` as a variable name.
- Large outputs bloat memory and callback logs — redirect to a file or use `no_log`.

## Verify
- [ ] `-v` output shows the keys you reference.
- [ ] Conditions use status tests (`is failed`) rather than `.rc == 0` where the module provides `failed`.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5.
- Confirmed: the common return values `backup_file`, `changed`, `diff`, `failed`, `invocation`, `msg`, `rc`, `results`, `skipped`, `stderr`, `stderr_lines`, `stdout`, `stdout_lines`, `ansible_facts`, `exception`, `warnings`, `deprecations`; the looped `results` structure with `msg: All items completed`; registered variables are host-level, in-memory and last for the rest of the run; failed or skipped tasks still register; the `is failed/changed/succeeded/skipped` tests; register projections and `_task` are new in 2.21.
- Fixed: `invocation` is not limited to `-vvv` (only `exception` is shown at `-vvv`).
- Removed as unconfirmed: the trailing-newline remark and the `selectattr` pipeline.

Method: documentation only; no commands were run.
