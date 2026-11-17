---
id: computing-software.cloud-infrastructure-engineering.ansible.filters-and-data-transformation
name: filters-and-data-transformation
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, filters, filter-plugins, jinja2-filters, json-query, jmespath, combine, selectattr, rejectattr, map, dict2items, items2dict, default, mandatory, regex-replace, regex-search, from-json, to-json, from-yaml, to-nice-yaml, ipaddr, ansible-utils, hash-merge, flatten, unique, zip, b64encode, password-hash, data-transformation, path-filters, hash-filter]
level: advanced
status: docs-checked
description: "Transform data in Ansible with filters: selectattr/map chains, combine recursive merge, dict2items/items2dict, json_query, regex, ipaddr, type coercion, and when to write a custom filter instead."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_filters.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/filter/combine.yml", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/filter/random.yml", "https://github.com/ansible-collections/community.general/blob/main/plugins/filter/json_query.py", "https://github.com/ansible-collections/ansible.utils/blob/main/plugins/filter/ipaddr.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/porting_guides/porting_guide_core_2.21.rst"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Filters and data transformation

**Goal:** reshape inventory and API data into the exact structure a module wants, in
one readable expression, instead of in a dozen `set_fact` tasks. Filters run on the control node.

## 1. The core toolkit
```yaml
# list of dicts -> filter -> project a field
web_ips: "{{ groups['web'] | map('extract', hostvars, ['ansible_host']) | list }}"
active:  "{{ users | selectattr('state', 'equalto', 'present') | map(attribute='name') | list }}"
no_admins: "{{ users | rejectattr('groups', 'contains', 'wheel') | list }}"
# dict <-> list
"{{ ports | dict2items }}"                        # [{key:.., value:..}]
"{{ pairs | items2dict(key_name='name', value_name='ip') }}"
# merge defaults with overrides (deep)
cfg: "{{ app_defaults | combine(app_env_overrides, recursive=true, list_merge='append') }}"
# strings
"{{ 'ansible' | regex_replace('^a.*i(.*)$', 'a\\1') }}"
"{{ version | regex_search('^[0-9]+[.][0-9]+') }}"
"{{ name | lower | replace(' ', '-') }}"
# types
"{{ port | int }}", "{{ flag | bool }}", "{{ raw | from_json }}", "{{ data | to_nice_yaml(indent=2) }}"
# lists
"{{ a | union(b) }}", "{{ a | difference(b) }}", "{{ nested | flatten }}", "{{ l | unique | sort }}"
"{{ names | zip(ips) | list }}", "{{ items | batch(3) | list }}", "{{ l | first }}", "{{ l | last }}"
# defaults and guards
"{{ x | default('n/a') }}", "{{ x | default(omit) }}", "{{ x | mandatory }}"
# paths, hashes, encoding
"{{ p | basename }}", "{{ p | dirname }}", "{{ s | b64encode }}", "{{ s | hash('sha256') }}"
"{{ pw | password_hash('sha512', 65534 | random(seed=inventory_hostname) | string) }}"
# networking (ansible.utils, needs the netaddr Python package)
"{{ '192.0.2.1/24' | ansible.utils.ipaddr('address') }}", "{{ subnet | ansible.utils.nthhost(5) }}"
```
`combine` options: `recursive` (default false) and `list_merge` (`replace` default, `keep`, `append`, `prepend`, `append_rp`, `prepend_rp`).
`map(attribute='a.b')` walks nested keys. `selectattr` tests include `equalto`, `defined`, `match`, `search`, `in`, `contains`, `truthy`.
`map` and `select` give generators; the documentation examples end the chain with `| list`.

## 2. json_query (JMESPath)
`community.general.json_query` needs the `jmespath` Python package on the control node (otherwise: `You need to install "jmespath" prior to running json_query filter`):
```yaml
"{{ ec2.instances | community.general.json_query('[?tags.Role==`db`].private_ip_address') }}"
"{{ data | community.general.json_query('services[].{name: name, port: ports[0]}') }}"
```
JMESPath literal strings are written with backticks inside a single-quoted query, as above, or with doubled single quotes (`''cluster1''`) inside a single-quoted YAML scalar. Prefer `selectattr` for simple cases and `json_query` for deep projections.

## 3. Multi-step reshaping without set_fact soup
Chain inside one `vars:` block on the task, which keeps the intermediate names local:
```yaml
- ansible.builtin.template: {src: hosts.j2, dest: /etc/hosts.d/cluster}
  vars:
    cluster_hosts: "{{ groups['cluster'] | map('extract', hostvars) | list }}"
    host_lines: "{{ cluster_hosts | map(attribute='ansible_host') | zip(cluster_hosts | map(attribute='inventory_hostname')) | list }}"
```
Task `vars` are evaluated lazily when referenced (unlike `set_fact`, which templates once on assignment), so order does not matter.

## 4. Building dicts
Build a dict from two lists with `dict(keys_list | zip(values_list))`, as in the documentation:
```yaml
ip_by_host: "{{ dict(groups['web'] | zip(groups['web'] | map('extract', hostvars, 'ansible_host'))) }}"
```
or accumulate in a loop: `set_fact: m: "{{ m | default({}) | combine({item.name: item.ip}) }}"`.

## 5. When to write a filter plugin
If an expression chains many filters, or you re-implement the same reshaping in several roles, put the logic in a filter plugin (a Python function in a collection's `plugins/filter/` directory). See the plugin-development skill.

## Gotchas
- `default` triggers on *undefined*; `default('x', true)` also replaces empty or false values.
- `combine` without `recursive=true` replaces nested dicts wholesale. The `hash_behaviour` setting (default `replace`) can make all variable merging recursive, but the configuration documentation warns against changing it: use `combine` instead.
- `regex_replace` takes a Python regular expression; in a Jinja string literal a backreference is written `'\\1'`, as in the documentation examples.
- `random` without `seed` changes every run, giving non-idempotent results; pass `seed=inventory_hostname` as the documentation does.
- `ipaddr` and the other network filters live in the `ansible.utils` collection and need `netaddr`.
- Filters run on the control node and cannot see the managed node's filesystem.
- Since ansible-core 2.21 `password_hash` output differs from earlier releases for the same input, because hashing moved from passlib to libcrypt; hashes stay valid.

## Verify
- [ ] Render the expression with a debug task and test data for edge cases (empty list, missing key).
- [ ] Every `map`/`select` chain ends in `| list`.
- [ ] Two consecutive runs are `changed=0` (no unseeded `random`, no unordered output in templates).

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed in the Using filters page (`extract`, `combine` options, `password_hash` with seeded `random`, `regex_replace` backreference form, `dict(keys | zip(values))`, json_query backtick and doubled-quote forms, jmespath dependency, ipaddr in ansible.utils) and the filter DOCUMENTATION blocks (`dict2items`, `items2dict`, `flatten`, `zip`, `random`, `regex_search`, `mandatory`, `hash`) and `DEFAULT_HASH_BEHAVIOUR` in `config/base.yml`; the community.general json_query and ansible.utils ipaddr/nthhost sources; the 2.21 porting guide for `password_hash`. Removed pinned counts for plugin size and the `from_yaml` vault claim.
Method: documentation only; no commands were run.
