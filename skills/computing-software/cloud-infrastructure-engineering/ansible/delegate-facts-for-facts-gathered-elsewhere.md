---
id: computing-software.cloud-infrastructure-engineering.ansible.delegate-facts-for-facts-gathered-elsewhere
name: delegate-facts-for-facts-gathered-elsewhere
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, delegation, delegate-facts, setup, hostvars, fact-gathering]
level: advanced
status: docs-checked
description: "Gather facts from hosts outside the play with setup plus delegate_to and delegate_facts, so templates can read hostvars of database or load balancer hosts."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html#delegating-facts", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/setup_module.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# delegate_facts: facts gathered elsewhere

Problem: a play on `app` hosts renders a config needing the IP address of `db1`, but db1 is not
in the play, so it has no facts.

## Default behaviour of delegation
Any facts gathered by a delegated task are assigned by default to the `inventory_hostname` (the current
host), not to the host that produced them (the delegated-to host). A delegated `setup` without
`delegate_facts` therefore attaches the delegate's facts to the app host.

## The pattern
```yaml
- hosts: app
  tasks:
    - name: Gather facts from DB servers
      ansible.builtin.setup:
        gather_subset: [network]
      delegate_to: "{{ item }}"
      delegate_facts: true
      loop: "{{ groups['dbservers'] }}"
      run_once: true

    - name: Render DB connection config
      ansible.builtin.template:
        src: db.conf.j2      # uses hostvars[groups['dbservers'][0]]['ansible_default_ipv4']['address']
        dest: /etc/app/db.conf
```
`delegate_facts: true` assigns the gathered facts to the delegate, so
`hostvars['dbhost1']['ansible_default_ipv4']['address']` works even though the db group is not in the
play or is excluded by `--limit`. `run_once` stops the gathering from repeating for every app host
(`run_once` applies results to all hosts in the batch unless `delegate_facts: true` is set).

Also works for `set_fact`:
```yaml
- ansible.builtin.set_fact:
    primary_lsn: "{{ lsn.stdout }}"
  delegate_to: db1
  delegate_facts: true
```

## Alternatives
- A preceding play on the db hosts with `gather_facts: true`.
- A persistent fact cache: `gathering = smart` or `explicit` use the cache plugin (facts from earlier
  runs, possibly stale).
- Inventory variables for static data such as an address from `ansible_host`.

## Gotchas
- Without `delegate_facts`, facts from the delegated `setup` are attached to the current host, so
  templates see the wrong values.
- A delegated-to host must be reachable with its own connection variables, because the connection variables
  of the delegate are used.
- `delegate_facts` is for facts; registered variables stay on the current host.

## Verify
- [ ] `debug: var=hostvars['dbhost1']['ansible_default_ipv4']['address']` prints the db IP.
- [ ] `debug: var=ansible_facts.hostname` on an app host still prints the app host's name.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_delegation.rst "Delegating facts", playbooks_strategies.rst
run_once notes) and ansible-core devel `config/base.yml` (`DEFAULT_GATHERING`) and `modules/setup.py`
(`gather_subset`). Removed unconfirmed claims about `--limit` reachability, `register` interaction, per-connection cost of a
preceding play, and the "app hosts become db hosts" symptom wording.
Method: documentation only; no commands were run.
