---
id: computing-software.cloud-infrastructure-engineering.ansible.variable-scope-global-play-and-host
name: variable-scope-global-play-and-host
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, variables-precedence, variable-scope, scoping, set-fact, hostvars, cacheable]
level: practitioner
status: docs-checked
description: "Reason about Ansible variable scope: global (config, -e), play (vars, vars_files, roles), host (inventory, facts, set_fact, register), and pass data between hosts and plays."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_variables.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_strategies.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/modules/set_fact.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_templating_now.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable scope: global, play, host

The Using variables page describes three main scopes:
| Scope | Set by |
|---|---|
| Global | configuration, environment variables and the command line (`-e` extra vars) |
| Play | each play and its contained structures: `vars`, `vars_files`, `vars_prompt`, role defaults and role vars |
| Host | variables directly associated with a host: inventory, `host_vars`/`group_vars`, `include_vars`, facts and registered task output (plus `set_fact`) |
Block and task `vars:` apply only to that block or task.

## Passing data between plays
Play variables are not mapped to hosts (and so not to `hostvars`). Host-scoped data survives into later plays:
```yaml
- hosts: db[0]
  tasks:
    - ansible.builtin.command: /opt/app/bin/gen-token
      register: token_out
    - ansible.builtin.set_fact:
        app_token: "{{ token_out.stdout }}"

- hosts: web
  tasks:
    - ansible.builtin.template: {src: app.env.j2, dest: /etc/app.env}
      vars:
        token: "{{ hostvars[groups['db'][0]]['app_token'] }}"
```

## Sharing a value with all hosts
Use a dummy host:
```yaml
- ansible.builtin.add_host:
    name: shared
    release_id: "{{ now(fmt='%Y%m%d%H%M') }}"
  run_once: true
# later: hostvars['shared'].release_id
```
`run_once` runs the task on the first host of the current batch and applies all results and facts to all hosts in that batch, so `set_fact` with `run_once: true` also assigns the value to every host in the batch.

## set_fact cacheable
`set_fact: {x: 1, cacheable: true}` also writes the value as a fact into the fact cache (it does not enable caching by itself). The variable keeps `set_fact` precedence for the current run and uses cached-fact precedence in later runs, which is lower. The module notes that `set_fact` values are templated once, on assignment, unlike normal lazy variables.

## Role vars leakage
By default (`private_role_vars` false), imported roles publish their variables to the play and to other roles. Set `private_role_vars = true` under `[defaults]` (`ANSIBLE_PRIVATE_ROLE_VARS`) to avoid that. Since 2.17, `include_role` and `import_role` take a `public` option to override the setting for that role; included roles only make their variables public at execution time, imported roles at playbook compile time.

## Gotchas
- Task `vars:` are lazy: they are evaluated when referenced, so `vars: {ts: "{{ now() }}"}` can differ between uses. Use `set_fact` to freeze a value.
- In the precedence list, registered vars and `set_fact` rank above `include_vars` and role vars, but below role and include params and extra vars.
- `hostvars['x']` for a host not in the play has its inventory variables but no facts unless they were gathered or cached.

## Verify
- [ ] `debug: var=hostvars[inventory_hostname]` in a later play shows the passed value.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on Using variables ("Scoping variables", the precedence list), the Controlling playbook execution page (`run_once` applies results and facts to the batch), the `set_fact` module documentation (`cacheable`, templated on assignment), `DEFAULT_PRIVATE_ROLE_VARS` in `config/base.yml`, the `now` function page and Using variables for host-versus-play mapping. Removed `include_params`, the numeric precedence labels and the `date` pipe lookup.
Method: documentation only; no commands were run.
