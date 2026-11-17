---
id: computing-software.cloud-infrastructure-engineering.ansible.how-limit-intersects-play-hosts
name: how-limit-intersects-play-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, host-patterns, limit-intersection, limit, multi-play]
level: practitioner
status: docs-checked
description: "Understand how --limit intersects with each play's hosts, how it affects multi-play playbooks, delegate_to, run_once and facts from hosts outside the limit."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_patterns.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/reference_appendices/special_variables.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_delegation.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_strategies.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/inventory/manager.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# How --limit intersects the play hosts

`--limit` (`-l`) restricts the hosts of **every play** in the run: the hosts a play runs on are the hosts its `hosts:` pattern selects, narrowed by the limit pattern. The limit "will reference your inventory" and cannot add hosts the play does not name.

```bash
ansible-playbook site.yml --limit web01
```
- Play `hosts: webservers` runs on web01 (if web01 is in `webservers`).
- Play `hosts: dbservers` selects no host in the limit, so it shows "skipping: no hosts matched" (not an error).
- The magic variable `ansible_limit` holds the contents of the `--limit` option for the current run.

## Consequences
- Multi-play orchestration (DB migrate, then web deploy, then load balancer) skips the plays whose groups are outside the limit. Document the limit the playbook needs.
- Facts of hosts outside the limit are not gathered: `hostvars['db01']['ansible_facts']` is empty unless a fact cache has them or you gather them with `setup` plus `delegate_to` and `delegate_facts: true`. The delegation documentation shows exactly this to look up `hostvars` for hosts "left out by using `--limit`".
- `run_once` runs the task on the first host of the current batch and applies the results and facts to all hosts in that batch.
- `groups['web']` lists the inventory's group members (the `groups` magic variable is described as all the groups in inventory), not the limited set. For the hosts in this run use `ansible_play_hosts` (hosts in the current play run, failed and unreachable hosts excluded) or `ansible_play_hosts_all` (all hosts targeted by the play).

## Limit syntax
```bash
--limit 'web:&prod'
--limit @retry_hosts.txt      # file of host names; prefix the file name with @
--limit 'web[0:2]'
```
The documentation also shows `--limit @site.retry` for the retry file written when `RETRY_FILES_ENABLED` is true. Use one pattern, with comma or colon separators, rather than several `--limit` flags.

## Verify
```bash
ansible-playbook site.yml --limit web01 --list-hosts     # per-play host lists
```

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the Patterns page (`--limit`, `@file`, retry file, "will reference your inventory"), the Special variables page (`ansible_limit`, `ansible_play_hosts`, `ansible_play_hosts_all`, `groups`), the Delegation page (`delegate_facts` for hosts excluded by `--limit`, `run_once`) and the Controlling playbook execution page (`run_once`), and `inventory/manager.py` (`subset`, `@file` handling). Removed unconfirmed statements about `delegate_to` ignoring the limit, localhost plays and the `ANSIBLE_LIMIT` environment variable (no such setting exists in `config/base.yml`).
Method: documentation only; no commands were run.
