---
id: computing-software.cloud-infrastructure-engineering.ansible.fact-gathering-policy-and-subsets
name: fact-gathering-policy-and-subsets
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, facts, smart-gathering, gathering-policy, gather-subset, fact-caching, gather-facts]
level: practitioner
status: docs-checked
description: "Choose the fact gathering policy (implicit, explicit, smart), limit gather_subset, and pair smart gathering with a fact cache to cut playbook start-up time."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-gathering", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/setup_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/gather_facts_module.html", "https://docs.ansible.com/ansible/latest/plugins/cache.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fact gathering policy and subsets

## The three policies (`[defaults] gathering` / `ANSIBLE_GATHERING`)
| Value | Behaviour |
|---|---|
| `implicit` (default) | the cache plugin is ignored; gather at the start of every play unless `gather_facts: false` |
| `explicit` | do not gather unless the play requests it |
| `smart` | scan each host that has no facts yet; a host addressed in several plays is not contacted again in the run |

`smart` and `explicit` use the fact cache plugin.

The default cache plugin is `memory`, so facts do not persist between runs; `smart` then still saves repeat gathering in multi-play playbooks, and a persistent plugin extends the saving across runs.

```ini
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = ~/.cache/ansible/facts
fact_caching_timeout = 7200      # seconds; default 86400
```

## Collect less
```yaml
- hosts: all
  gather_facts: true
  gather_subset: ['!all', '!min', network, virtual]   # or: [min]
  gather_timeout: 20      # per-fact-module timeout in seconds (default 10)
```
Subsets include `all`, `hardware`, `network`, `virtual`, `ohai` and `facter` plus finer ones such as
`distribution`, `pkg_mgr`, `service_mgr`, `mounts`, `devices` and `interfaces`. `!all` leaves only the `min` subset; use `!all,!min` to skip even that. Prefix a value with `!` to exclude it.
To apply a subset to many plays, use `module_defaults` for the `setup` module or the play-level `gather_subset` keyword.

## Gathering explicitly
```yaml
- hosts: web
  gather_facts: false
  tasks:
    - ansible.builtin.wait_for_connection:
    - ansible.builtin.setup:
        gather_subset: [network]
        filter: ['ansible_default_ipv4', 'ansible_hostname']
```
`filter` takes shell-style (fnmatch) patterns and limits which keys are returned (a list since 2.11; an empty list means no filter).

## Cache hygiene
- Facts in the cache go stale (IP changed, disk added). `ansible-playbook --flush-cache` clears the fact cache for every host in the inventory.

## Gotchas
- With `smart`, a task that changes system state (installs a package, adds an interface) leaves cached facts stale; re-run `setup` after such changes.
- The `gather_facts` action runs the configured facts modules (`FACTS_MODULES`, default `setup`); `ansible_facts_parallel` controls whether several fact modules run in parallel.

## Verify
- [ ] Second run with `smart` shows no "Gathering Facts" task for cached hosts (or near-zero time in `profile_tasks`).
- [ ] The directory in `fact_caching_connection` has one file per host (jsonfile plugin).

## Checked
Checked 2026-10-25 against ansible-core devel `config/base.yml` (DEFAULT_GATHERING choices, CACHE_PLUGIN, CACHE_PLUGIN_TIMEOUT), the `setup` and `gather_facts` module documentation, `cli/arguments/option_helpers.py` (`--flush-cache`) and `playbook/play.py` (play keywords), commit of 2026-10. Confirmed: policy names and meanings, cache keys and defaults, `gather_timeout` default 10, `gather_subset` semantics including `!all,!min`, `filter` list form (2.11), `--flush-cache` scope. Removed unconfirmed claims about a `[defaults] gather_subset` setting, Redis settings, `always` tagging of the setup task, Windows setup module, hostvars access to cached hosts and the 0 = never expire timeout.
Method: documentation only; no commands were run.
