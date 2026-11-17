---
id: computing-software.cloud-infrastructure-engineering.ansible.generating-host-inventory-documentation
name: generating-host-inventory-documentation
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, iac-documentation, inventory-docs, ansible-cmdb, fact-tree, host-reports, ansible-inventory-graph, cmdb-export]
level: practitioner
status: draft
description: "Generate always-current host and inventory documentation from Ansible facts and inventory: ansible-cmdb HTML/CSV reports, ansible-inventory graphs, and templated per-host pages."
sources: ["ansible-cmdb project documentation (https://github.com/fboender/ansible-cmdb)", "Ansible documentation - ansible-inventory CLI and setup module --tree output (https://docs.ansible.com/ansible/latest/cli/ansible-inventory.html)", "Ansible documentation - Fact caching"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generating host and inventory documentation

Goal: an inventory/host overview (OS, versions, IPs, memory, disks, groups, custom vars) that is
regenerated from reality on a schedule instead of a wiki page nobody updates.

## 1. Collect facts
```bash
ansible all -i inventories/prod -m ansible.builtin.setup --tree out/facts/
```
One JSON file per host. Alternatively reuse the jsonfile fact cache directory.

## 2a. ansible-cmdb (quick, static HTML)
```bash
pip install ansible-cmdb
ansible-cmdb -i inventories/prod out/facts/ > out/hosts.html             # default html_fancy template
ansible-cmdb -t csv -i inventories/prod out/facts/ > out/hosts.csv
ansible-cmdb -t markdown out/facts/ > out/hosts.md
ansible-cmdb -t html_fancy -c name,os,ip,mem,cpus,disk_usage out/facts/ > out/hosts-short.html
```
`-i` adds inventory groups and host vars to the report; `-f` includes custom facts from
`facts.d`. Templates: `html_fancy`, `html_fancy_split` (one file per host — use for large
fleets), `txt_table`, `csv`, `json`, `markdown`, `sql` (load into a DB for queries).
ansible-cmdb is a community tool with slow upstream activity; pin the version and keep a
fallback (2b).

## 2b. Your own template (full control)
```yaml
- hosts: all
  gather_facts: true
  tasks:
    - ansible.builtin.template:
        src: hosts.md.j2
        dest: "{{ playbook_dir }}/out/hosts.md"
      delegate_to: localhost
      run_once: true
```
```jinja
| Host | OS | IP | vCPU | RAM GB | Groups |
|---|---|---|---|---|---|
{% for h in ansible_play_hosts_all | sort %}{% set f = hostvars[h].ansible_facts %}
| {{ h }} | {{ f.distribution }} {{ f.distribution_version }} | {{ f.default_ipv4.address | default('-') }} | {{ f.processor_vcpus }} | {{ (f.memtotal_mb / 1024) | round(1) }} | {{ hostvars[h].group_names | join(', ') }} |
{% endfor %}
```

## 3. Inventory structure
```bash
ansible-inventory -i inventories/prod --graph > out/inventory-tree.txt
ansible-inventory -i inventories/prod --list --export --yaml > out/inventory-export.yml
```

## Publish
Schedule (CI or a controller job) daily; publish `out/` to an internal static site or commit to
a docs repo so changes show up as diffs ("RAM on db03 changed").

## Gotchas
- Facts contain sensitive data (IPs, MACs, users, sometimes env vars); publish to an access-controlled location and strip fields you don't need.
- Unreachable hosts produce no fact file and silently disappear from the report; list `dark` hosts explicitly.
- Fact-gathering the whole fleet daily is load; use `gather_subset: [hardware, network, virtual]`.

## Verify
- [ ] Report host count equals `ansible-inventory --list | jq '._meta.hostvars|length'` minus listed unreachable hosts.
- [ ] A change on a host (RAM, OS update) appears in the next report.
