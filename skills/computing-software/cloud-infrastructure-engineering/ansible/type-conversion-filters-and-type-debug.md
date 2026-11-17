---
id: computing-software.cloud-infrastructure-engineering.ansible.type-conversion-filters-and-type-debug
name: type-conversion-filters-and-type-debug
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, filters, type-debug, bool-filter, int-filter, from-json, from-yaml, to-nice-yaml]
level: practitioner
status: docs-checked
description: "Find a value's real type with type_debug and convert it with int, float, bool, string, list, from_json, from_yaml, to_json and to_nice_yaml before comparing or templating."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type conversion filters and type_debug

## Find out what you have
```yaml
- ansible.builtin.debug:
    msg: "{{ some_var | type_debug }}"     # shows the underlying Python type name
```
Compare types with the `string`, `number`, `mapping`, `sequence` and `boolean` tests rather than against `type_debug` output.

## Where wrong types come from
- `-e key=value` values are interpreted as strings; use JSON (`-e '{"port": 8080}'`) to pass integers, booleans, floats or lists.
- A `vars_prompt` answer is a string, so a boolean prompt needs `| bool`.
- A registered variable may hold a dictionary where the next task needs a list; convert with `dict2items` or `items2dict`.
- Fact values such as `distribution_major_version` are strings, so cast with `| int` before numeric comparison.

## Converting
```yaml
"{{ port | int }}"            "{{ ratio | float }}"      "{{ flag | bool }}"
"{{ 8080 | string }}"         "{{ x | list }}"           # list() of a string splits into characters!
"{{ result.stdout | from_json }}"                       # parse JSON output of a CLI
"{{ lookup('file', 'cfg.yml') | from_yaml }}"
"{{ docs | from_yaml_all | list }}"                     # multi-document YAML
"{{ data | to_json }}"   "{{ data | to_nice_json(indent=2) }}"
"{{ data | to_yaml }}"   "{{ data | to_nice_yaml(indent=2, width=1000) }}"
```
`bool` maps `yes/on/1/true` → True and `no/off/0/false` → False (string comparison is case-insensitive); an invalid value produces a deprecation warning, and the `truthy` / `falsy` tests are the more permissive alternative.

`int` of a non-number returns `0` silently (Jinja's default, overridable with `int(default)`): `'abc' | int` → 0. Validate untrusted input with `regex('^\\d+$')` first. `int` takes a `base` argument for prefixed or hex strings.

## Rendering config files
- JSON configs: `{{ cfg | to_nice_json }}` — always valid JSON; never hand-write JSON in Jinja.
- YAML configs: `to_nice_yaml` accepts `indent`, `width` (preferred line width; raise it to avoid folding of long strings) and `sort_keys` (default True).
- `to_nice_json` also accepts `sort_keys` and `indent`.

## Gotchas
- Comparing `'8' == 8` is False — the most common "when never matches" bug.
- `list` of a string splits it into characters, so use `split` for delimited strings.

## Verify
- [ ] `type_debug` on every input that crosses a boundary (-e, survey, stdout) during development.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Filters (playbooks_filters.rst), ansible-core plugins/filter docs, Templating now() page, Jinja filters.py; Variables page; Jinja filters.py do_int.
Confirmed:
- type_debug; -e key=value values are strings; bool accepted values and deprecation warning; int returns 0 by default and takes a base; to_nice_yaml and to_nice_json options; from_yaml_all.
- Removed the AnsibleUnsafeText names, jinja2_native paragraph, from_json-empty and !unsafe claims.

Method: documentation only; no commands were run.
