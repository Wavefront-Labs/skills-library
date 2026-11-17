---
id: computing-software.cloud-infrastructure-engineering.ansible.host-pattern-quoting-and-gotchas
name: host-pattern-quoting-and-gotchas
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, host-patterns, pattern-quoting, limit, ipv6]
level: intro
status: docs-checked
description: "Avoid host pattern mistakes: shell quoting of ! and &, comma vs colon separators, IPv6 addresses, ranges vs slices and patterns that silently match nothing."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_patterns.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/reference_appendices/YAMLSyntax.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host pattern quoting and gotchas

## Quote every non-trivial pattern
```bash
ansible 'web:!web03' -m ping            # bash history expansion would eat ! in double quotes
ansible 'web:&prod' -m ping              # an unquoted & is a shell operator
ansible 'web*' -m ping                   # an unquoted * can glob against local files
ansible-playbook site.yml --limit 'db:!db-replica*'
```
The Patterns page says single quotes MUST be used with a negated limit to prevent bash interpolation.

## Separators
- `:` and `,` both separate patterns: `web:db` equals `web,db`.
- Prefer `,` when IPv6 addresses or ranges are involved: `'2001:db8::10,2001:db8::11'`. The documentation states that the comma is preferred with ranges and IPv6; the colon form is kept for backward compatibility and cannot always tell an address from a separator.
- In `hosts:` YAML, quote a pattern that starts with `*`, `&` or `!`: these characters cannot start an unquoted YAML scalar. For example write `hosts: '*.example.com'` and `hosts: 'web:&prod'` with quotes.

## Ranges vs slices
- Inventory ranges such as `web[01:20].example.com` are a definition syntax in inventory files; ranges are inclusive.
- Pattern slices `web[0:4]` and `web[-1]` index into a group's host list at run time (zero based, the end index is included).

## Silent nothing
- A typo in a group name logs `[WARNING]: Could not match supplied host pattern, ignoring: wbe` and the run continues. A play with no matching hosts shows as "skipping: no hosts matched", which is success with nothing done. To fail instead, set `host_pattern_mismatch = error` in the `[inventory]` section of `ansible.cfg` (or `ANSIBLE_HOST_PATTERN_MISMATCH=error`); the default is `warning`.
- Use `--list-hosts` and assert a count in CI.

## Operator precedence
Order in the pattern does not matter: Ansible applies unions (`:` and `,`), then intersections (`&`), then exclusions (`!`).

## Verify
```bash
ansible 'web:&prod:!web03' --list-hosts
```

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the Patterns page (single quotes, comma preferred, processing order, slices, warning text), the YAML syntax page (characters that cannot start an unquoted scalar), the inventory guide (ranges are inclusive) and `config/base.yml` (`HOST_PATTERN_MISMATCH` default `warning`, choices include `error` and `ignore`). Removed the case-sensitivity claim.
Method: documentation only; no commands were run.
