---
id: computing-software.cloud-infrastructure-engineering.ansible.reading-other-hosts-facts-via-hostvars
name: reading-other-hosts-facts-via-hostvars
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, facts-magic-vars, hostvars-other-hosts, hostvars, delegate-facts]
level: practitioner
status: docs-checked
description: "Read facts and variables of other hosts through hostvars, ensure they were gathered in the same run or cache, and build cluster configs from group members."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_vars_facts.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_delegation.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/reference_appendices/special_variables.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/porting_guides/porting_guide_core_2.20.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Facts of other hosts via hostvars

```jinja
{# templates/haproxy.cfg.j2 #}
backend web
{% for h in groups['web'] %}
    server {{ h }} {{ hostvars[h]['ansible_facts']['default_ipv4']['address'] }}:8080 check
{% endfor %}
```

## The facts must exist
`hostvars` gives access to variables defined for any host in the play, but facts only after they have been gathered or cached. The Ansible documentation says you "must either cache facts or gather facts for those hosts before the task that fills out the template". Options:
```yaml
# 1. Gather in an earlier play
- hosts: web
  gather_facts: true
  tasks: []
- hosts: lb
  tasks: [...]

# 2. Gather on the fly for hosts outside the play
- ansible.builtin.setup:
    gather_subset: [network]
  delegate_to: "{{ item }}"
  delegate_facts: true
  loop: "{{ groups['web'] }}"
```
With `--limit lb01` the `web` play is skipped (the limit narrows every play), so option 2 or a fact cache is the robust choice; the delegation documentation shows option 2 for hosts "left out by using `--limit`".

## Safe access
```jinja
{{ hostvars[h].ansible_facts.default_ipv4.address | default(hostvars[h].ansible_host) }}
```
Inventory variables of other hosts (`hostvars[h].ansible_host`, group variables) are available without gathering; only facts need gathering or caching. Variables defined at play level are not mapped to `hostvars`.

## Patterns
- Cluster member lists: `groups['etcd'] | map('extract', hostvars, ['ansible_facts','default_ipv4','address']) | list` (the `extract` filter takes a container and a list of subkeys).
- Primary selection: `groups['db'] | first`.

## Gotchas
- For "hosts in this run" use `ansible_play_hosts` (active hosts of the play run), not `groups[...]`, which lists the inventory group.
- Fact names: use the `ansible_facts[...]` form; top-level `ansible_*` fact variables depend on `inject_facts_as_vars`, whose default (true) is deprecated and changes to false in ansible-core 2.24.

## Verify
```yaml
- ansible.builtin.debug:
    msg: "{{ groups['web'] | map('extract', hostvars, ['ansible_facts','default_ipv4','address']) | list }}"
  run_once: true
```

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the Discovering variables page (magic variables and `hostvars`, gather or cache first, play variables not in `hostvars`), the Delegation page (`delegate_facts`, hosts excluded by `--limit`), the Special variables page, the Using filters page (`extract`, chained undefined with `default`) and the 2.20 porting guide (`INJECT_FACTS_AS_VARS`). Removed the claim about how `hostvars` values are templated for other hosts, which the documentation does not state.
Method: documentation only; no commands were run.
