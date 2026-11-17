---
id: computing-software.cloud-infrastructure-engineering.ansible.looping-over-inventory-groups-and-hostvars
name: looping-over-inventory-groups-and-hostvars
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, loops, loop-hosts, loop-groups, hostvars, inventory-hostnames, ansible-play-hosts]
level: practitioner
status: docs-checked
description: "Iterate over hosts in a group or play with groups, ansible_play_hosts and inventory_hostnames, and read each host's vars via hostvars for configs like /etc/hosts or upstreams."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/reference_appendices/special_variables.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_loops.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_delegation.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_vars_facts.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Looping over groups and hostvars

## Sources of host lists
| Expression | Gives |
|---|---|
| `groups['web']` | the hosts of group `web` from the inventory |
| `groups['all']` | every inventory host |
| `ansible_play_hosts` | hosts in the current play run, not limited by `serial`; failed and unreachable hosts are excluded |
| `ansible_play_hosts_all` | all hosts targeted by the play |
| `ansible_play_batch` | active hosts in the current `serial` batch (equal to `ansible_play_hosts` when `serial` is not set) |
| `query('inventory_hostnames', 'web:&prod:!web3')` | hosts matching a full pattern (`all:!www` in the documentation's example) |

## Typical use: build configs from other hosts' data
```yaml
- name: Render /etc/hosts entries for the cluster
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: '\s{{ item }}$'
    line: "{{ hostvars[item]['ansible_facts']['default_ipv4']['address'] }} {{ item }}"
  loop: "{{ groups['cluster'] }}"
```
In a template (usually better, one file change instead of N tasks):
```jinja
upstream app {
{% for h in groups['app'] | sort %}
  server {{ hostvars[h].ansible_host | default(h) }}:{{ hostvars[h].app_port | default(8080) }};
{% endfor %}
}
```

## Facts of other hosts must exist
`hostvars[h]['ansible_facts']` is empty unless facts for `h` were gathered earlier in the run or a fact cache holds them. Options:
- target the group in an earlier play: `- hosts: app` with `gather_facts: true`
- gather on the fly: `ansible.builtin.setup` with `delegate_to: "{{ item }}"`, `delegate_facts: true` and `loop: "{{ groups['app'] }}"`. The delegation documentation says this assigns the facts to the delegated hosts and lets you look up `hostvars` even for hosts "left out by using `--limit`".
- use inventory variables (`ansible_host`) instead of facts where possible

## Reduce to one host doing the work
```yaml
- name: Create DB users for every app host
  community.postgresql.postgresql_user:
    name: "app_{{ item | replace('.', '_') }}"
  loop: "{{ groups['app'] }}"
  run_once: true
  delegate_to: "{{ groups['db'][0] }}"
```
The documentation shows `run_once: true` with a loop over `ansible_play_hosts_all` for work that must happen once for every host.

## Gotchas
- `groups` is described as the groups in the inventory with their hosts, so when you mean "hosts in this run" use `ansible_play_hosts`, which reflects the play's hosts and drops failed or unreachable ones.
- Group order follows the compiled inventory, which the documentation calls "reproducible ... not normally predictable": `| sort` for stable templates and no spurious changes.

## Verify
- [ ] `ansible-inventory --graph cluster` matches the loop input.
- [ ] The template renders unchanged on a second run (stable ordering).

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the Special variables page (`groups`, `ansible_play_hosts`, `ansible_play_hosts_all`, `ansible_play_batch`), the Loops page (`inventory_hostnames` pattern use), the Delegation page (`delegate_facts`, `run_once` with `ansible_play_hosts_all`), the Using variables page (`hostvars` and facts need gathering or caching) and the Controlling playbook execution page (inventory order). Removed the claim about `groups` and `--limit` interaction beyond the documented wording, the `groups['missing']` error claim, and the unsourced "ignores `--limit`" table note.
Method: documentation only; no commands were run.
