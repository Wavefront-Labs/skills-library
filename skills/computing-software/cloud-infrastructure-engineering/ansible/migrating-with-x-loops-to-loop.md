---
id: computing-software.cloud-infrastructure-engineering.ansible.migrating-with-x-loops-to-loop
name: migrating-with-x-loops-to-loop
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, loops, with-x-migration, loop-migration, with-items, with-dict, subelements, dict2items]
level: practitioner
status: docs-checked
description: "Convert legacy with_items, with_dict, with_subelements, with_nested, with_sequence and with_fileglob to loop plus filters or query(), preserving behaviour."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating with_X to loop

`with_*` is not deprecated and stays valid for the foreseeable future; `loop` (added in 2.5) is recommended for most use cases. Convert carefully: `with_items` flattens one level, `loop` does not.

| Legacy | loop equivalent |
|---|---|
| `with_list: "{{ x }}"` | `loop: "{{ x }}"` |
| `with_items: "{{ x }}"` | `loop: "{{ x | flatten(levels=1) }}"` |
| `with_indexed_items` | `loop: "{{ x | flatten(levels=1) }}"` + `loop_control: {index_var: idx}` |
| `with_flattened` | `loop: "{{ x | flatten }}"` |
| `with_together: [a, b]` | `loop: "{{ a | zip(b) | list }}"` → `item.0`, `item.1` |
| `with_dict: "{{ d }}"` | `loop: "{{ d | dict2items }}"` → `item.key`, `item.value` |
| `with_subelements: ["{{ users }}", keys]` | `loop: "{{ users | subelements('keys', skip_missing=True) }}"` (`skip_missing` is optional) |
| `with_nested: [a, b]` / `with_cartesian` | `loop: "{{ a | product(b) | list }}"` |
| `with_sequence: start=0 end=4 stride=2 format=testuser%02x` | `loop: "{{ range(0, 4 + 1, 2) | list }}"` with `"{{ 'testuser%02x' | format(item) }}"` in the body (range excludes its end point) |
| `with_random_choice: "{{ x }}"` | `"{{ x | random }}"` (no loop) |
| `with_fileglob: "*.conf"` | keep `with_fileglob` (or `loop` with `query('ansible.builtin.fileglob', ...)`) |
| `with_dict: "{{ d }}"` (alternative) | `loop: "{{ d | dictsort }}"` → `item.0`, `item.1` |

A `with_*` that needs `lookup` inside the loop (for example `with_fileglob`) should stay as it is rather than become `loop: "{{ lookup('fileglob', '*.txt', wantlist=True) }}"`. Where you do pass a lookup to `loop`, use `query()`: it always returns a list, whereas `lookup()` returns a comma-joined string unless `wantlist=True`.

## Example
```yaml
# before
- ansible.posix.authorized_key: {user: "{{ item.0.name }}", key: "{{ item.1 }}"}
  with_subelements: [ "{{ users }}", keys ]
# after
- ansible.posix.authorized_key: {user: "{{ item.0.name }}", key: "{{ item.1 }}"}
  loop: "{{ users | subelements('keys') }}"
  loop_control: {label: "{{ item.0.name }}"}
```

## Also migrate loop helpers
- `loop_control.index_var` replaces `with_indexed_items` indexes.
- `loop_control.extended: true` gives `ansible_loop.index0`, `first`, `last`, `length` and more.
- `until` with `retries` applies per item of the loop.

## Gotchas
- `with_items` on a list of lists flattened it — a straight swap to `loop` changes `item` from a string to a list. Use `flatten(levels=1)`.
- `with_dict` has two documented replacements: `dict2items` (`item.key`, `item.value`) and `dictsort` (`item.0`, `item.1`); pick the one whose item shape your task uses.
- `loop` does not accept a string as input; a lookup passed to it must return a list (`query`, or `wantlist=True`).
- The `sequence` lookup generates strings, while `range()` produces integers; convert where the body relies on the type.

## Verify
- [ ] Run before and after with `--check -v` and compare item lists (`loop_control.label`).
- [ ] `with_` no longer appears in the migrated files, except for deliberate `with_<lookup>` forms.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Loops (playbooks_loops.rst, shared_snippets/with2loop.txt), devel; lookup plugin sources.
Confirmed:
- Every conversion row now follows the documented with2loop snippet (list, items, indexed_items, flattened, together, dict with dict2items or dictsort, sequence with range, subelements, nested/cartesian with product, random_choice with random).
- loop added in 2.5, with_ not deprecated; keep with_ forms that need lookup; query versus lookup.
- Removed first_found and generic with_lookup rows and the lazy-templating claim.

Method: documentation only; no commands were run.
