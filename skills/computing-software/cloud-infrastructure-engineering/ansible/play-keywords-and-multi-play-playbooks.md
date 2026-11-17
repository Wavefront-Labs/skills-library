---
id: computing-software.cloud-infrastructure-engineering.ansible.play-keywords-and-multi-play-playbooks
name: play-keywords-and-multi-play-playbooks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, playbook-syntax, play-keywords, play-level-keywords, multiple-plays, multi-play, pre-tasks, post-tasks]
level: practitioner
status: docs-checked
description: "Structure a playbook as several plays with the right play-level keywords (hosts, become, vars, pre_tasks, roles, tasks, post_tasks) and understand their execution order."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html", "https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html#play", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html", "https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Play keywords and multi-play playbooks

A playbook is a YAML list of plays. Each play maps a host pattern to work; plays run top to
bottom, each finishing on all its hosts before the next starts.

## A multi-play rolling deploy
```yaml
- name: Take web nodes out of the load balancer
  hosts: web
  serial: 1
  gather_facts: false
  tasks:
    - community.general.haproxy: {state: disabled, host: "{{ inventory_hostname }}", backend: app}
      delegate_to: "{{ item }}"
      loop: "{{ groups.lb }}"

- name: Migrate the database once
  hosts: db[0]
  become: true
  tasks:
    - ansible.builtin.command: app-migrate
      register: mig
      changed_when: "'No migrations' not in mig.stdout"

- name: Configure web nodes
  hosts: web
  become: true
  vars_files: [vars/app.yml]
  pre_tasks:
    - ansible.builtin.apt: {update_cache: true, cache_valid_time: 3600}
  roles:
    - common
    - nginx
  tasks:
    - ansible.builtin.include_tasks: deploy.yml
  post_tasks:
    - ansible.builtin.uri: {url: "http://{{ inventory_hostname }}/health", status_code: 200}
```

## Order inside one play
1. implicit play-level tasks first (fact gathering with `gather_facts`, argument validation)
2. `pre_tasks`, then handlers they triggered
3. `roles` in the order listed (each role's `dependencies` run first, subject to tag filtering and conditionals)
4. `tasks`, then handlers triggered by roles or tasks
5. `post_tasks`, then their handlers

## Play keywords worth knowing
| Keyword | Use |
|---|---|
| `hosts`, `order`, `serial`, `strategy`, `throttle` | which hosts and how they are batched |
| `gather_facts`, `gather_subset`, `gather_timeout`, `fact_path` | fact collection |
| `become`, `become_user`, `become_method`, `remote_user`, `connection`, `port` | how to connect |
| `vars`, `vars_files`, `vars_prompt` | play-scoped variables |
| `module_defaults`, `environment`, `collections` | defaults applied to every task |
| `any_errors_fatal`, `max_fail_percentage`, `ignore_errors`, `ignore_unreachable`, `force_handlers` | failure policy |
| `tags`, `check_mode`, `diff`, `no_log`, `run_once`, `debugger` | inherited by all tasks |

The full list is in `ansible-doc -t keyword -l` (and `ansible-doc -t keyword serial`). The keywords in the table are the attributes ansible-core defines for plays (the `Play` class plus the shared base, tags and collections attributes).

## Variables across plays
`vars:` of one play are not visible in the next. To pass data: `set_fact` (lives on the host, so
next play reads `hostvars['db1'].migration_id`), or `add_host`/`group_by` to build groups for later plays.
`import_playbook` composes playbook files: `- ansible.builtin.import_playbook: webservers.yml`.

## Gotchas
- A host pattern that matches nothing is governed by `host_pattern_mismatch` (ansible.cfg `[inventory]`, default `warning`; it can be set to error or ignore).
- Play-level `tags` tag every task in the play; a tag on a `roles:` entry applies to all tasks of that role.
- `vars:` set in a play have play (object) scope; values set with `set_fact` or `include_vars` are host scope and reach later plays.

## Verify
- [ ] `ansible-playbook site.yml --list-tasks` shows the plays and task order you expect.
- [ ] `--list-hosts` per play confirms targets.

## Checked
Checked 2026-10-25 against ansible-core devel `playbook/play.py` and `playbook/base.py` attribute lists (every keyword in the table is a play-level attribute), `config/base.yml` (HOST_PATTERN_MISMATCH), and ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_reuse_roles.rst (execution order, handlers flush), playbooks_startnstep.rst (implicit play-level tasks) and reference_appendices/general_precedence.rst (variable scope across plays). Confirmed: keyword names, order of pre_tasks, roles, tasks and post_tasks with handler flushes, dependency ordering, and cross-play variable scope. Removed unconfirmed claims about `vars_files` path resolution and fact gathering being tagged `always`; replaced a host-specific command path with a plain command name.
Method: documentation only; no commands were run.
