---
id: computing-software.cloud-infrastructure-engineering.ansible.facts-custom-facts-and-magic-variables
name: facts-custom-facts-and-magic-variables
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, facts, gather-facts, setup-module, gather-subset, custom-facts, facts-d, local-facts, magic-variables, hostvars, groups, group-names, inventory-hostname, ansible-play-hosts, fact-caching, jsonfile-cache, redis-cache, cacheable, set-fact, ansible-facts, inject-facts-as-vars, special-variables]
level: practitioner
status: docs-checked
description: "Gather, cache and shape Ansible facts: gather_subset, facts.d custom facts, set_fact cacheable, fact caching, and magic variables (hostvars, groups) for cross-host data."
sources: ["Discovering variables: facts and magic variables (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html)", "Special variables (https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html)", "ansible.builtin.setup module source (https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/setup.py)", "ansible.builtin.set_fact module source (https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/set_fact.py)", "Configuration settings source, DEFAULT_GATHERING and INJECT_FACTS_AS_VARS (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)", "Cache plugins (https://docs.ansible.com/ansible/latest/plugins/cache.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Facts, custom facts and magic variables

**Goal:** playbooks that use what the host really is (OS, IPs, memory, your own
metadata), without paying 5-10 seconds per host per play to collect it, and that can
reach data from other hosts (e.g. the DB primary's IP) safely.

## 1. Gathering and trimming
```yaml
- hosts: all
  gather_facts: true            # default; runs ansible.builtin.setup
  gather_subset: ['!all', '!min', 'network', 'virtual']   # only what you need
```
Subsets (setup module docs): `all`, `min`, `hardware`, `network`, `virtual`, `ohai`, `facter`, plus individual fact names. `!all` collects only `min`; `!all,!min` collects only the subsets you list; `!hardware` skips the hardware facts. The setup module's `gather_timeout` defaults to 10 seconds per fact collector. Inspect a host: `ansible h -m setup -a 'filter=ansible_default_ipv4'`.

Facts live under `ansible_facts.<name>` and (with `inject_facts_as_vars = True`, the default)
also as `ansible_<name>`. Prefer `ansible_facts['distribution']`, which works whatever that setting is.

## 2. Custom facts (facts.d)
On the managed node, any `*.fact` file in `/etc/ansible/facts.d/` that is INI, JSON, or an
executable printing JSON shows up under `ansible_local`:
```ini
# /etc/ansible/facts.d/app.fact
[deploy]
version=2.3.1
owner=platform
```
→ `{{ ansible_local.app.deploy.version }}`. Deploy the file with `copy` and then re-run
`setup` (or `gather_facts`) in the same play — facts are gathered at play start, so a
fact file written in task 3 is not visible until you `ansible.builtin.setup: filter=ansible_local`.
Executable fact scripts are a clean way to expose app health or licence state to playbooks.

## 3. set_fact and cacheable
`set_fact` creates a host-scoped variable at high precedence that lasts for the run.
`cacheable: true` also adds it to the fact cache. It does not turn fact caching on; it only works if a cache is configured. The variable keeps `set_fact` precedence for the current run and gets cached-fact precedence in later runs.

## 4. Fact caching
```ini
[defaults]
gathering = smart            # gather only when no cached facts
fact_caching = jsonfile      # or a plugin from a collection, e.g. community.general.redis
fact_caching_connection = /tmp/ansible-facts
fact_caching_timeout = 7200  # seconds
```
`smart` and `explicit` use the cache plugin; with `smart`, a host that already has facts is not contacted again. Cached facts also let `hostvars[other]` work for hosts not in the current play. `ansible-playbook --flush-cache` clears the fact cache for every host in inventory. The default cache plugin is `memory`, which lasts only for the current run.

## 5. Magic variables (the ones you actually use)
| Variable | Meaning |
|---|---|
| `inventory_hostname` / `inventory_hostname_short` | name from inventory (not the host's own hostname — that is `ansible_facts.hostname`) |
| `hostvars['db01']['ansible_facts']['default_ipv4']['address']` | any host's vars/facts — facts only if gathered or cached |
| `groups['web']`, `groups['all']` | host lists per group |
| `group_names` | groups the current host is in |
| `ansible_play_hosts` / `ansible_play_hosts_all` | hosts still active in the play (failed or unreachable excluded) / all hosts targeted by the play |
| `ansible_play_batch` | active hosts in the current `serial` batch |
| `play_hosts` (deprecated, same as `ansible_play_batch`), `ansible_limit`, `ansible_run_tags` | invocation details (`--limit`, `--tags`) |
| `playbook_dir`, `role_path`, `inventory_dir`, `ansible_config_file` | paths |
| `ansible_check_mode`, `ansible_diff_mode`, `ansible_version` | run flags |
| `omit` | leave a module parameter unset: `mode: "{{ file_mode | default(omit) }}"` |

Cross-host pattern (DB primary's IP into app config):
```yaml
db_host: "{{ hostvars[groups['db'][0]].ansible_facts.default_ipv4.address }}"
```
Requires the `db` hosts' facts to be gathered in this run or cached; otherwise the lookup fails with an undefined-attribute error.
Add a first play `- hosts: db\n  gather_facts: true\n  tasks: []` when needed.

## Gotchas
- `ansible_default_ipv4` is the interface of the default route, not necessarily the one you want; pick by `ansible_facts.interfaces` or use `ansible_host`.
- Facts are per host; a `set_fact` on host A is not visible on host B except via `hostvars['A']`.
- `gather_facts: false` and then referencing `ansible_facts.os_family` fails with an undefined-variable error, not an empty value.
- Caching stale facts across a reboot/IP change is a classic cause of "it worked yesterday".

## Verify
- [ ] `ansible h -m setup -a 'gather_subset=!all,!min,network' | wc -l` is a fraction of the full output and the play still has every fact it references.
- [ ] `ansible h -m setup -a 'filter=ansible_local'` shows the `ansible_local.*` values from facts.d.
- [ ] With `gathering = smart` the second run of a 50-host play skips the `Gathering Facts` task.

## Checked

Checked 2026-10-26 against ansible-core 2.21.5 sources (devel branch, 2026-10-23) and ansible-documentation main (2026-10-21).
- Confirmed from the setup module: subset names, `!all` / `!all,!min` semantics, `gather_timeout` default 10, `fact_path` default for facts.d `*.fact` files (executable files run, others read; JSON or INI) feeding `ansible_local`.
- Confirmed: `gathering` values `implicit`, `explicit`, `smart` and that smart/explicit use the cache plugin; `inject_facts_as_vars` default True; `set_fact` `cacheable` precedence; `--flush-cache` help text; magic variable names and meanings in the special variables page (`play_hosts` deprecated).
- Removed as unconfirmed: the speed claims, the exact Jinja error text, the Windows subset remark, and the claim that fact-var injection is going away.

Method: documentation only; no commands were run.
