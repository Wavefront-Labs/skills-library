---
id: computing-software.cloud-infrastructure-engineering.ansible.set-fact-cacheable-and-fact-precedence
name: set-fact-cacheable-and-fact-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, variables-precedence, set-fact-cacheable, set-fact, fact-caching]
level: practitioner
status: docs-checked
description: "Use set_fact with cacheable: true to persist computed values in the fact cache across plays and runs, and understand the precedence change it causes."
sources: ["ansible.builtin.set_fact module (https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html)", "Ansible variables guide, variable precedence (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence)", "Ansible facts guide, caching facts (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html#caching-facts)", "ansible.builtin.jsonfile cache plugin (https://docs.ansible.com/ansible/latest/collections/ansible/builtin/jsonfile_cache.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# set_fact cacheable

```yaml
- name: Look up the release
  ansible.builtin.uri:
    url: "{{ release_api }}"
    return_content: true
  register: release_info

- name: Keep the computed value for later runs
  ansible.builtin.set_fact:
    app_release: "{{ release_info.json.tag_name }}"
    cacheable: true
```

## What cacheable does
- Normal `set_fact`: a host variable at precedence level 19 ("Registered vars and set_facts" in the variable precedence list), kept for the rest of the run and available to later plays.
- `cacheable: true`: also turns the value into a fact that is added to the fact cache. It does **not** enable fact caching by itself; it only works with it when a persistent cache plugin is already configured.
- The module creates two copies: the normal `set_fact` host variable with high precedence, and a lower-precedence fact copy that can persist through the cache plugin. In a later run the value loaded from the cache has host-fact precedence (level 11 in the list), below play vars and role vars, so a value that won in one run can lose in the next.
- `meta: clear_facts` removes the fact copy but not the host variable.

## Config for persistence
```ini
[defaults]
gathering = smart
fact_caching = ansible.builtin.jsonfile
fact_caching_connection = .facts_cache
fact_caching_timeout = 86400
```
`smart` and `explicit` gathering use the cache plugin. The default cache plugin is `memory`, which keeps facts only for the current run. The `jsonfile` plugin writes one JSON file per host into the `fact_caching_connection` directory; the timeout default is 86400 seconds.

## Gotchas
- With the default `memory` cache, `cacheable` has no effect across runs.
- Cached values can go stale; set `fact_caching_timeout`. Cache files are plain JSON on disk, so do not store secrets in them.

## Verify
- [ ] After a run with `jsonfile` caching, the file for the host under the `fact_caching_connection` directory contains the cached value.

## Checked
Checked 2026-10-23 against the ansible-core source and the Ansible documentation source on GitHub (set_fact.py, playbooks_variables.rst, playbooks_vars_facts.rst, config/base.yml, plugins/cache/jsonfile.py; latest ansible-core release v2.21.5): the two-copy behaviour of `cacheable`, the precedence levels 19 and 11, the statement that it does not enable caching, `meta: clear_facts`, the `gathering`, `fact_caching`, `fact_caching_connection` and `fact_caching_timeout` options and defaults (memory plugin, 86400), and the jsonfile plugin's per-host JSON files. Replaced the example (it relied on `json_query`, which is not in ansible-core) and removed the unconfirmed constructed-inventory and controller fact-storage claims and the `jq` check.
Method: documentation only; no commands were run.
