---
id: computing-software.cloud-infrastructure-engineering.ansible.loop-inputs-flatten-range-sequence-and-fileglob
name: loop-inputs-flatten-range-sequence-and-fileglob
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, loops, loop-flatten, loop-range, with-sequence, with-fileglob]
level: intro
status: docs-checked
description: "Feed loops from flatten for nested lists, range and sequence for numbered items, and fileglob for control-node files, with the loop equivalents of with_ forms."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fileglob_lookup.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/sequence_lookup.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Loop inputs: flatten, range, sequence, fileglob

## Nested lists: flatten
```yaml
- ansible.builtin.dnf:
    name: "{{ item }}"
  loop: "{{ [base_packages, web_packages, extra_packages | default([])] | flatten }}"
```
`flatten(levels=1)` limits depth. Better still for packages: pass the flattened list directly to `name:` (the docs call this better than looping, because per-item loops are slower and may cause issues with interdependencies).
`with_items` performs implicit single-level flattening; `loop` does not, so migrated loops often need `| flatten(1)`.

## Numbers: range and sequence
```yaml
- ansible.builtin.file:
    path: "/data/disk{{ item }}"
    state: directory
  loop: "{{ range(1, 5) | list }}"              # 1..4 (end exclusive)

- ansible.builtin.debug: {msg: "{{ item }}"}
  loop: "{{ query('ansible.builtin.sequence', 'start=0 end=20 stride=5 format=node%02d') }}"
  # node00 node05 node10 node15 node20 (end inclusive)
```
`range` is Python-like (end exclusive). `sequence` takes `start`, `end` (or `count`), `stride` and a printf-style `format`; numbers may be decimal, hex (`0x3f8`) or octal (`0600`). Its generated items are strings, so convert with `| int` for arithmetic.

## Control-node files: fileglob
```yaml
- ansible.builtin.copy:
    src: "{{ item }}"
    dest: /etc/pki/ca-trust/source/anchors/
  loop: "{{ query('ansible.builtin.fileglob', 'files/certs/*.crt') }}"
  notify: update ca trust
```
- Matches local files on the **control node** in a single directory, non-recursively, using Python's `glob`; relative paths follow the task path search rules (role `files/` directory first, then the task file's and play file's directories).
- A pattern matches files only, not directories. No match returns an empty list, so the loop silently does nothing. For files on a managed node use `ansible.builtin.find`.
- The loop documentation says that a `with_*` that needs `lookup` inside a loop should stay as is, so `with_fileglob: 'files/certs/*.crt'` is an equally valid form.

## Gotchas
- `lookup('fileglob', ...)` returns a comma-joined string; use `query()` or `wantlist=True` for loops.
- Pass `range(...)` through `| list`, as the documented examples do.

## Verify
```yaml
- ansible.builtin.debug: {msg: "{{ query('ansible.builtin.fileglob', 'files/certs/*.crt') }}"}
```

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Loops (playbooks_loops.rst, shared_snippets/with2loop.txt), devel; lookup plugin sources.
Confirmed:
- with_items flattening and flatten(levels=1); range end exclusive; sequence lookup options, hex and octal numbers, string items; fileglob non-recursive, controller-side, empty list on no match.
- The documented advice to keep with_fileglob rather than converting a lookup inside loop.
- Removed the filetree reference.

Method: documentation only; no commands were run.
