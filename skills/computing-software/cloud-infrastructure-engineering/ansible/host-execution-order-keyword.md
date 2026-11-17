---
id: computing-software.cloud-infrastructure-engineering.ansible.host-execution-order-keyword
name: host-execution-order-keyword
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, playbook-syntax, strategies-forks, play-order, host-order, inventory-order, order-keyword, serial]
level: practitioner
status: docs-checked
description: "Control the order in which hosts are processed in a play with the order keyword (inventory, sorted, reverse_sorted, reverse_inventory, shuffle) and combine it with serial."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html", "https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host execution order: the order keyword

`order` is a play keyword that decides the sequence in which hosts are fed to the strategy:

| Value | Order |
|---|---|
| `inventory` (default) | order returned for the selection from the compiled inventory |
| `reverse_inventory` | reverse of inventory |
| `sorted` | alphabetical by inventory name |
| `reverse_sorted` | reverse alphabetical |
| `shuffle` | random each run |

```yaml
- hosts: web
  order: sorted
  serial: 2
  tasks: ...
```

## Where it matters
Order has visible effect only when hosts are batched or limited:
- **serial batches**: with `serial: 2` and `order: sorted`, batch 1 is web01+web02, deterministically. With dynamic inventory the default order can change run to run; set `sorted` for predictable rolling updates.
- **run_once**: the task runs on the first host of the current batch, so order decides which one that is.
- **shuffle**: spread load (e.g. package mirror pressure) or uncover hidden ordering dependencies.

Plays themselves always run in file order; tasks within a play run in file order. `order` only
affects hosts.

## Patterns
Canary first, then the rest, deterministically:
```yaml
- hosts: web
  order: sorted
  serial: [1, "25%", "100%"]
```
Reverse a rollout (upgrade standby side first): `order: reverse_inventory`.

## Gotchas
- `sorted` is string sort: `web10` sorts before `web2`. Zero-pad host names (`web02`) or build an explicit group.
- The `inventory` value is the order in which the compiled inventory returns the selection; it is reproducible but not necessarily the file definition order.

## Verify
- [ ] Run output shows batch membership matches the intended canary.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Controlling playbook execution (playbooks_strategies.rst) and Error handling (playbooks_error_handling.rst), devel; ansible-core helpers.py, play.py, special_variables.rst.
Confirmed:
- order values inventory, reverse_inventory, sorted, reverse_sorted, shuffle; inventory order is the compiled-inventory order, not file order; run_once uses the first host of the batch.
- Removed claims about forks, groups order in Jinja, free strategy and --list-hosts.

Method: documentation only; no commands were run.
