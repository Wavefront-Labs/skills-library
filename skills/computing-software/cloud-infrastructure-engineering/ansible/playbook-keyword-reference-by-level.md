---
id: computing-software.cloud-infrastructure-engineering.ansible.playbook-keyword-reference-by-level
name: playbook-keyword-reference-by-level
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, playbook-syntax, keyword-reference, play-keywords, ansible-doc]
level: practitioner
status: docs-checked
description: "Use the playbook keyword reference to see which keywords are valid at play, role, block and task level, and read keyword docs offline with ansible-doc -t keyword."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html", "https://docs.ansible.com/ansible/latest/cli/ansible-doc.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/playbook/play.py", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/playbook/block.py", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/playbook/task.py", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/playbook/base.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Playbook keyword reference by level

The keywords page lists every keyword valid at **Play**, **Role**, **Block** and **Task** level. Check applicability with `ansible-doc -t keyword <name>` before using a keyword at a new level.

## Offline lookup
```bash
ansible-doc -t keyword -l              # list all keywords
ansible-doc -t keyword serial          # description and applies_to
ansible-doc -t keyword -j throttle     # JSON, including where it applies
```

## Keywords by level (most used)
Derived from the playbook classes in ansible-core 2.22 (role-level use was not checked).

| Keyword | Play | Block | Task |
|---|---|---|---|
| hosts, gather_facts, gather_subset, gather_timeout, fact_path, serial, strategy, max_fail_percentage, order, vars_files, vars_prompt, roles, pre_tasks, tasks, post_tasks, handlers, force_handlers | yes | | |
| name, become*, check_mode, diff, environment, ignore_errors, ignore_unreachable, module_defaults, no_log, tags, vars, any_errors_fatal, run_once, throttle, timeout, collections, debugger, connection, remote_user, port | yes | yes | yes |
| when, delegate_to, delegate_facts, notify | | yes | yes |
| block, rescue, always | | yes | |
| loop, loop_control, register, until, retries, delay, changed_when, failed_when, async, poll, args, action, local_action | | | yes |

`run_once` and `throttle` are valid on plays; `when`, `delegate_to` and `notify` are not (the Play class has only the base, tags and collections keywords).

## Inheritance
Keywords set on a play, role or block are inherited by contained tasks; task values override.

## Gotchas
- `vars_files` exists only at play level; roles use `vars/` and include_vars.
- `name` is valid everywhere and should be set everywhere.
- A misspelt keyword at task level may be read as a module name, so run `--syntax-check`.

## Verify
```bash
ansible-playbook site.yml --syntax-check
```

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed from lib/ansible/playbook (stable-2.22): Play defines hosts, gather_facts, gather_subset, gather_timeout, fact_path, vars_files, vars_prompt, roles, handlers, pre_tasks, post_tasks, tasks, force_handlers, max_fail_percentage, serial, strategy, order and derives from Base, Taggable and CollectionSearch only; Block and Task add Conditional, Notifiable and Delegatable; Task alone defines args, action, async, changed_when, delay, failed_when, loop, loop_control, poll, register, retries, until; Base defines name, connection, port, remote_user, vars, module_defaults, environment, no_log, run_once, ignore_errors, ignore_unreachable, check_mode, diff, any_errors_fatal, throttle, timeout, debugger and the become options; ansible-doc keyword output reports where each keyword applies (cli/doc.py).
- Removed unconfirmed claims: the verbatim error messages, the when/tags accumulation exceptions, the role column and the jq filter.

Method: documentation only; no commands were run.
