---
id: computing-software.cloud-infrastructure-engineering.ansible.list-filters-unique-union-difference-zip
name: list-filters-unique-union-difference-zip
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, filters, list-filters, set-theory-filters, zip]
level: practitioner
status: docs-checked
description: "Manipulate lists with unique, union, intersect, difference, symmetric_difference, zip, zip_longest, batch, first, last, min, max and sum for inventory and package logic."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# List filters

## Set theory
```yaml
all_pkgs: "{{ (base_pkgs + role_pkgs) | unique }}"
to_remove: "{{ installed_users | difference(allowed_users) }}"
common: "{{ groups['web'] | intersect(groups['prod']) }}"
either: "{{ list_a | union(list_b) }}"              # unique union
changed_either_side: "{{ list_a | symmetric_difference(list_b) }}"
```
`union` and `symmetric_difference` return items in arbitrary order; add `| sort` where output order matters (templates, idempotence).

## Pairing
```yaml
# zip: pair two lists (stops at the shorter list)
pairs: "{{ disks | zip(mountpoints) | list }}"           # [['sdb','/data1'], ['sdc','/data2']]
# build a dict from two lists
disk_map: "{{ dict(disks | zip(mountpoints)) }}"
# zip_longest runs to the longest list and fills gaps with fillvalue
"{{ a | zip_longest(b, fillvalue='-') | list }}"
```

## Slicing and aggregates
```yaml
first_db: "{{ groups['db'] | first }}"
newest: "{{ releases | sort | last }}"
batches: "{{ groups['web'] | batch(5) | list }}"         # lists of 5
total_mb: "{{ volumes | map(attribute='size_mb') | sum }}"
largest: "{{ volumes | max(attribute='size_mb') }}"
count: "{{ users | length }}"
flat: "{{ nested | flatten(levels=1) }}"
```

## Membership and filtering
```yaml
"{{ 'nginx' in installed_packages }}"
"{{ users | select('match', '^svc-') | list }}"
"{{ ports | difference([22, 443]) }}"
```

## Gotchas
- `unique` accepts `attribute=` (uniqueness by that attribute of each object) and `case_sensitive=` (default false).
- `map`, `select` and `zip` return iterators; add `| list` before indexing or taking `length`, as the documented zip examples do.

## Verify
```yaml
- ansible.builtin.debug: {msg: "{{ to_remove }}"}
```

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Filters (playbooks_filters.rst), ansible-core plugins/filter docs, Templating now() page, Jinja filters.py.
Confirmed:
- unique options attribute and case_sensitive; union and symmetric_difference return arbitrary order; zip stops at the shorter list, zip_longest takes fillvalue; min and max take attribute from 2.11; flatten levels; first, last, sum, batch, select and reject are Jinja builtins.
- Removed the Jinja 3.0 remark and the reject('in') example.

Method: documentation only; no commands were run.
