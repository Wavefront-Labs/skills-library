---
id: computing-software.cloud-infrastructure-engineering.ansible.debugger-keyword-and-task-debugger
name: debugger-keyword-and-task-debugger
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, debugging, debugger-keyword, enable-task-debugger, debugger]
level: practitioner
status: docs-checked
description: "Turn on the task debugger with the debugger keyword (on_failed, on_unreachable, always) or ANSIBLE_ENABLE_TASK_DEBUGGER, then inspect and fix task args and vars live."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_debugger.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html#enable-task-debugger"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The debugger keyword

## Enable
```yaml
- hosts: web
  debugger: on_failed            # play-wide
  tasks:
    - name: Deploy
      ansible.builtin.template: {src: app.j2, dest: /etc/app.conf}
      debugger: always           # task-level overrides play
```
Values: `always`, `never`, `on_failed`, `on_unreachable`, `on_skipped`. Valid on plays, roles, blocks and tasks (since 2.5); the most granular definition wins, and the keyword overrides the global setting.

Globally without editing playbooks:
```bash
ANSIBLE_ENABLE_TASK_DEBUGGER=True ansible-playbook site.yml      # debugger on failed tasks
```
or `[defaults] enable_task_debugger = True`. Only `True`/`False` are accepted; a failed task invokes the debugger unless the role, play, block or task disables it. By default the debugger honours `ignore_errors` (`task_debugger_ignore_errors = True`). The legacy `strategy: debug` still works but may be removed.

## Session commands
```
[web01] TASK: Deploy (debug)> p task.args
{'src': 'app.j2', 'dest': '/etc/app.conf'}
[web01] TASK: Deploy (debug)> p task_vars['app_port']
[web01] TASK: Deploy (debug)> p result._result
[web01] TASK: Deploy (debug)> task.args['dest'] = '/etc/app/app.conf'
[web01] TASK: Deploy (debug)> task_vars['app_port'] = 8081
[web01] TASK: Deploy (debug)> update_task      # re-template task with changed vars
[web01] TASK: Deploy (debug)> redo             # run the task again
[web01] TASK: Deploy (debug)> continue         # c: move on
[web01] TASK: Deploy (debug)> quit             # q: abort the play
```
There are seven commands: `print` (`p`, accepts `task`, `task.args`, `task_vars`, `host`, `result`), `task.args[key] = value`, `task_vars[key] = value` (follow with `update_task`), `update_task` (`u`), `redo` (`r`), `continue` (`c`), `quit` (`q`, aborts the playbook).

## When to use
- Failing template/module args you cannot see easily: inspect rendered args and result.
- Trying a fix without rerunning a 20-minute play from the start.
- Remember to apply the fix in code afterwards; debugger changes are not saved.

## Gotchas
- With the `linear` strategy Ansible halts while the debugger is active. With `free`, queued tasks stay queued and run as soon as you leave the debugger, and after `redo` other queued tasks may run before the rescheduled one.

## Verify
- [ ] `redo` after changing `task.args` produces the expected result.

## Checked
Checked 2026-10-25 against the ansible-documentation devel branch (commit of 2026-10-21) playbook_guide/playbooks_debugger.rst and ansible-core `config/base.yml` (ENABLE_TASK_DEBUGGER, TASK_DEBUGGER_IGNORE_ERRORS). Confirmed: keyword values and scope, override rules, config and environment names, the seven commands and shortcuts, the `update_task` requirement and free-strategy behaviour. Removed unconfirmed claims about TTY requirements, CI use, interleaving workarounds and `on_skipped` noise.
Method: documentation only; no commands were run.
