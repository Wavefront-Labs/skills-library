---
id: computing-software.cloud-infrastructure-engineering.ansible.host-pattern-syntax-wildcards-sets-slices-regex
name: host-pattern-syntax-wildcards-sets-slices-regex
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, host-patterns, pattern-intersection, pattern-exclusion, regex-patterns, pattern-regex, pattern-slice, group-index, wildcard-patterns, pattern-wildcards, limit]
level: practitioner
status: docs-checked
description: "Write Ansible host patterns precisely: union, intersection and exclusion, wildcards, group index slices and ~regex, with the processing order and shell quoting rules."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_patterns.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/inventory/manager.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host pattern syntax: sets, wildcards, slices, regex

A pattern appears in `hosts:` of a play, as the first argument of `ansible`, and in `--limit`.
Preview before running: `ansible-playbook site.yml --limit '<pattern>' --list-hosts`
or `ansible '<pattern>' -i inventory --list-hosts`.

## Set operations
| Pattern | Meaning |
|---|---|
| `web:db` or `web,db` | union: hosts in web OR db |
| `web:&staging` | intersection: in web AND staging |
| `web:!phoenix` | exclusion: in web but NOT phoenix |
| `web:db:&staging:!phoenix` | combined: (web or db) AND staging, NOT phoenix |

Processing order is fixed regardless of how you write it: `:`/`,` unions first, then `&`
intersections, then `!` exclusions (the documentation shows `a:b:&c:!d:!e == &c:a:!d:b:!e`). So
`web:&staging:db` is `(web ∪ db) ∩ staging`, not `(web ∩ staging) ∪ db`. If you need the other grouping, create a group in inventory or use two plays.

The comma is preferred over the colon when you use ranges or IPv6 addresses:
`--limit 'web1.example.com,2001:db8::1'`.

## Wildcards
Wildcards (`*.example.com`, `web-*`, `192.0.*`) are matched against host and group names in the inventory, translated with Python's `fnmatch` rules (so `?` and `[seq]` are special too). They match the **inventory name** (or alias), not `ansible_host`: a host listed as
`web1 ansible_host=192.0.2.10` is not matched by `192.0.2.*`, and an address that is not an inventory name gives "Could not match supplied host pattern". `all` and `*` are equivalent.

## Group index and slices
```
web[0]        # first host in group web
web[-1]       # last host
web[0:2]      # first THREE hosts - the end index is included
web[1:]       # all but the first
web[:3]       # web[0] to web[3]
```
Slicing the group with both ends omitted is an invalid pattern, and a start greater than the end gives an empty slice. Order is the group's order in the compiled inventory (the documentation calls it "reproducible ... not normally predictable"). Use slices for canaries: `--limit 'web[0]'` then `--limit 'web[1:]'`.

## Regular expressions
Start the pattern with `~`: `~(web|db).*\.example\.com`. The expression is applied with Python's `re.match`, so it is anchored at the **start** of the name but not the end: add `$` if you mean the whole name. Quote it in the shell.

## Variables in patterns
```yaml
- hosts: "{{ target | default('none') }}"
```
With `-e` you can pass group specifiers, as in the documentation's `webservers:!{{ excluded }}:&{{ required }}`. Defaulting `target` to a group that does not exist (`none`) turns a forgotten `-e target=...` into a no-match instead of a run against everything.

## Gotchas
- Bash expands `!` in double quotes: the documentation says single quotes MUST be used (`'all:!prod'`).
- A pattern made only of `&` and `!` terms works: the manager prepends `all`, so `'!prod'` means `all:!prod`. Writing `all:!prod` is clearer.
- A pattern that matches nothing logs "Could not match supplied host pattern, ignoring" and the run continues; a play with no matching hosts is shown as "skipping: no hosts matched". The `host_pattern_mismatch` setting (`ANSIBLE_HOST_PATTERN_MISMATCH`, `[inventory]` section, default `warning`) can be set to `error` or `ignore`.
- Group names with dashes are accepted but produce an invalid-group-name warning by default (`TRANSFORM_INVALID_GROUP_CHARS` defaults to `never`); prefer underscores.
- `--limit` further restricts the hosts a play targets; it never adds hosts the play does not name.

## Verify
- [ ] `--list-hosts` output equals the hosts you intended, count checked.
- [ ] Patterns with `!` are single-quoted in scripts and CI YAML.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the Patterns page (set operators and processing order, comma preferred, slices including the end index, `~` regex, single quotes for `!`, alias matching) and in `lib/ansible/inventory/manager.py` (`order_patterns` prepending `all`, `fnmatch.translate` and `re.match`, the mismatch message) and `config/base.yml` (`HOST_PATTERN_MISMATCH`, `TRANSFORM_INVALID_GROUP_CHARS`). Corrected: `!`/`&` can lead a pattern, regex uses match not search. Removed the case-sensitivity claim.
Method: documentation only; no commands were run.
