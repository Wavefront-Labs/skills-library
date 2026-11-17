---
id: computing-software.cloud-infrastructure-engineering.ansible.conditionals-and-loops
name: conditionals-and-loops
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, conditionals, when, loops, loop, loop-control, with-items, with-dict, dict2items, subelements, product, loop-var, label, pause, until, retries, delay, register, is-defined, is-failed, is-changed, os-family, index-var, extended-loop, flatten, nested-loops]
level: practitioner
status: docs-checked
description: "Write Ansible conditionals and loops: when with Jinja tests, loop and loop_control, product/subelements nesting, until/retries, and register results inside loops."
sources: ["Conditionals (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html)", "Loops (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)", "Tests (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tests.html)", "Reusing Ansible artifacts, include vs import (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse.html)", "ansible-lint rule no-jinja-when (https://github.com/ansible/ansible-lint/blob/main/src/ansiblelint/rules/no_jinja_when.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditionals and loops

**Goal:** tasks that run exactly where they should and iterate without 200-line
output or a quadratic blow-up.

## 1. `when`
`when` is a raw Jinja expression — **no** `{{ }}`:
```yaml
- ansible.builtin.dnf: name=httpd state=present
  when: ansible_facts['os_family'] == "RedHat" and ansible_facts['distribution_major_version'] | int >= 9
- ansible.builtin.debug: msg=ok
  when:                       # list = AND
    - result is defined
    - result.rc == 0
    - "'ERROR' not in result.stdout"
```
Idioms:
- `when: var is defined` / `is undefined` / `is none`; `when: var | default('') | length > 0` for "set and non-empty".
- `when: result is failed` / `is changed` / `is succeeded` / `is skipped` — always use these tests on registered results rather than `result.failed == true` (keys may be absent).
- `when: "'web' in group_names"`, `when: inventory_hostname == groups['db'][0]` (run once, on the first DB).
- `when: ansible_facts['pkg_mgr'] == 'apt'` beats matching distribution names.
- `when` on a `block` applies to every task inside; on an `import_*` statement the condition is copied to each imported task; on an `include_*` statement it applies only to the include task itself, not to the tasks inside.

A `when` that references a loop variable is evaluated per item (`when: item.enabled`).

## 2. `loop` basics
```yaml
- ansible.builtin.user:
    name: "{{ item.name }}"
    groups: "{{ item.groups | default(omit) }}"
  loop: "{{ app_users }}"
  loop_control:
    label: "{{ item.name }}"      # hide the full dict in output
```
- Lists: `loop: "{{ list }}"`; dicts: `loop: "{{ dict | dict2items }}"` → `item.key` / `item.value`.
- Nested: `loop: "{{ users | product(['dev','ops']) | list }}"` (item.0, item.1) or
  `loop: "{{ sites | subelements('aliases') }}"` for list-of-objects-with-lists.
- `loop: "{{ query('fileglob', 'files/*.conf') }}"` — `query` returns a list; `lookup(...)` returns a string unless `wantlist=True`.
- `loop_control`: `loop_var: svc` (mandatory when nested includes loop, else inner `item` shadows outer), `index_var: idx`, `pause: 2` (seconds between items), `extended: true` → `ansible_loop.index/first/last/length`.
- `with_items`, `with_dict`, `with_fileglob` still work but are lookup sugar; `loop` is the standard. `with_items` flattens one level implicitly, `loop` does not, so add `| flatten(levels=1)` when converting.

## 3. Loops over whole modules, not tasks
Most modules take lists natively — prefer that to a loop (one transaction, one changed, faster):
```yaml
- ansible.builtin.dnf: {name: ["httpd", "mod_ssl", "php"], state: present}   # not loop over dnf
```
Looping `include_tasks` runs a whole task file per item; `include_role` with `loop` is allowed too. `import_*` cannot loop.

## 4. Retry loops
```yaml
- ansible.builtin.uri: {url: "http://{{ inventory_hostname }}:8080/health"}
  register: health
  until: health.status == 200
  retries: 30
  delay: 5
```
`until` is a conditional on the registered result. The defaults are `retries: 3` and `delay: 5` (seconds); the task runs up to `retries` times and fails if `until` never becomes true. The registered result gets an `attempts` key recording how many attempts it took.

## 5. Register inside a loop
`register` in a loop yields `{results: [ {...per item..., item: <item>} ]}`. Use:
```yaml
- ansible.builtin.debug:
    msg: "{{ item.item.name }} rc={{ item.rc }}"
  loop: "{{ out.results }}"
  when: item is changed
```
The `results` list has one entry per item, each carrying the item under `item`.

## Gotchas
- `when: "{{ x }}"` — `{{ }}` is not needed in `when` (the expression is already evaluated as Jinja); ansible-lint flags it as `no-jinja-when`.
- Comparing versions: `ansible_facts.distribution_version is version('9.2', '>=')`.
- A looped task runs the module once per item on each host; where a module accepts a list natively (section 3), pass the list instead of looping.
- Loop var shadowing in nested `include_tasks` is the most common "wrong item" bug: always set `loop_var` on the outer loop.

## Verify
- [ ] `ansible-lint` reports no `no-jinja-when` or `literal-compare` findings.
- [ ] Output of a looped task shows your `label`, not whole dicts/secrets.
- [ ] Running the play with `--check` against a host of the other OS family skips the platform-specific tasks rather than failing.

## Checked

Checked 2026-10-26 against ansible-documentation main (last commit 2026-10-21) and ansible-core 2.21.5.
- Confirmed: `when` takes a bare expression; on `import_*` the condition is applied to each imported task but on `include_*` only to the include itself (the earlier text about `include_role` was wrong and is corrected); `import_*` cannot be used in a loop.
- Confirmed: `until` defaults are `retries: 3`, `delay: 5`, and the registered result has an `attempts` key; `loop_control` supports `label`, `loop_var`, `index_var`, `pause` and `extended`; `lookup` needs `wantlist=True` or `query` to return a list for `loop`; `with_items` flattens one level implicitly.
- Confirmed: the test names `failed`, `changed`, `succeeded`, `skipped` and `version`; the ansible-lint rules `no-jinja-when` and `literal-compare` exist.
- Removed as unconfirmed: string-boolean claim, early-exit behaviour of failed loop items, and the loop-size anecdote.

Method: documentation only; no commands were run.
