---
id: computing-software.cloud-infrastructure-engineering.ansible.debugging-playbooks-and-verbosity
name: debugging-playbooks-and-verbosity
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, debugging, debugger, debug-module, verbosity, callback-plugins, callback-result-format, yaml-callback, profile-tasks, timer, log-path, ansible-log, keep-remote-files, step, start-at-task, list-tasks, list-hosts, syntax-check, undefined-variable, troubleshooting, strategy-debug, debug-var, ssh-debug, debugger-commands]
level: practitioner
status: docs-checked
description: "Debug Ansible runs: debug and verbosity, the task debugger keyword, keeping remote module files to rerun by hand, readable callbacks, log_path, --step and --start-at-task."
sources: ["Debugging tasks (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_debugger.html)", "Debugging modules (https://docs.ansible.com/ansible/latest/dev_guide/debugging.html)", "Logging Ansible output (https://docs.ansible.com/ansible/latest/reference_appendices/logging.html)", "ansible-core CLI option help source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/arguments/option_helpers.py)", "result_format callback options source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/doc_fragments/result_format_callback.py)", "Callback plugins shipped in ansible-core (https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/callback)", "ansible.posix callback plugins (https://github.com/ansible-collections/ansible.posix/tree/main/plugins/callback)", "Configuration settings source (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Debugging playbooks and verbosity

**Goal:** find why a task failed or produced the wrong value in minutes, without
sprinkling the repo with `debug` tasks.

## 1. First look
```bash
ansible-playbook site.yml --syntax-check          # YAML/keyword errors
ansible-playbook site.yml --list-tasks --list-hosts -l web   # what would run, where
ansible-playbook site.yml --check --diff -l one-host          # dry run
ansible-playbook site.yml -vvv   # more v = more output; -vvv is a reasonable start, -vvvv for connection debugging
```
Per the CLI help, `-vvv` is a reasonable level to start with and `-vvvv` helps with connection problems. Add `ANSIBLE_CALLBACK_RESULT_FORMAT=yaml` (or
`callback_result_format = yaml` in `ansible.cfg`) so results are readable instead of JSON blobs.

## 2. Inspect variables
```yaml
- ansible.builtin.debug: {var: hostvars[inventory_hostname]}          # everything for this host
- ansible.builtin.debug: {msg: "{{ cfg | to_nice_yaml }}"}
- ansible.builtin.debug: {var: result, verbosity: 2}                  # only prints at -vv or more
```
`verbosity:` keeps permanent diagnostic tasks silent in normal runs. For precedence
questions use `ansible-inventory --host X` (inventory-level) and `debug: var=` at the
task (final). `ansible.builtin.assert` with `fail_msg` turns an assumption into a check.

## 3. The task debugger
Enable per task/play/role with `debugger: on_failed` (also `on_unreachable`, `on_skipped`,
`always`, `never`) or globally `ANSIBLE_ENABLE_TASK_DEBUGGER=True`. When the task fails you
drop into a prompt on the control node:
```
[db01] TASK: Render config (debug)> p task.args          # module args as templated
> p result._result                                       # the failure
> p host  /  p task_vars['db_port']
> task.args['dest'] = '/tmp/test.conf'                   # edit
> u                                                      # update_task: re-template
> r                                                      # redo
> c / q                                                  # continue / quit
```
Combine with `-vvv` to see the actual remote command.

## 4. Re-run the module by hand on the host
```bash
ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook site.yml -l db01 --start-at-task "Render config" -vvv
# on db01:
ls ~/.ansible/tmp/ansible-tmp-*/           # AnsiballZ_template.py
python3 AnsiballZ_template.py explode      # unpack
python3 AnsiballZ_template.py execute      # run with the same args
```
`explode` gives you `debug_dir/args` to tweak and the module source to add prints to.

## 5. Narrowing the run
`--start-at-task "name"`, `--step` (confirm each task before it runs), `--tags`/
`--skip-tags`, `-l host`, `-e debug_x=1` toggles.

## 6. Output and logs
- `log_path = ./ansible.log` (or `ANSIBLE_LOG_PATH`) saves Ansible output in one log on the control node; secrets in output end up in it unless tasks use `no_log` (ansible-core 2.22 also masks registered secrets there).
- `callbacks_enabled = ansible.posix.profile_tasks, ansible.posix.timer` prints per-task durations: the first thing to turn on for "it is slow".
- `display_args_to_stdout = True` adds the task arguments to each task header; the setting's own docs warn that this can print sensitive values.
- The `tree` callback (`ansible -t /tmp/out ...` for ad hoc runs) writes one file of results per host.
- `ANSIBLE_STDOUT_CALLBACK=ansible.builtin.minimal` or `ansible.builtin.oneline` for terse output; `ansible.posix.json` (shipped in the ansible.posix collection, not in ansible-core) gives JSON for CI parsers; `ansible.builtin.junit` writes JUnit XML.
- `ANSIBLE_DEBUG=1` is engine-level tracing — enormous; last resort.

## 7. Reading common errors
| Message | Meaning |
|---|---|
| `The task includes an option with an undefined variable` | typo or precedence; pass it with `-e` to confirm |
| `MODULE FAILURE` | the module crashed on the target; rerun with `-vvv` and, if needed, debug the module by hand (section 4) |

## Gotchas
- `debug` prints whatever it is given, so remove temporary debugs of vaulted values before commit. From ansible-core 2.22 registered secrets are masked as `$REDACTED$` in `debug` output at every verbosity level; earlier releases print them.
- `--start-at-task` skips `set_fact`/`register` tasks before it, so later references may be undefined.

## Verify
- [ ] With `callback_result_format = yaml` and `profile_tasks` enabled, a failed task shows a readable result and the slowest tasks are listed at the end.
- [ ] You can drop into the debugger with `debugger: on_failed`, print `task.args`, fix a value, `r`, and the task passes.
- [ ] `ANSIBLE_KEEP_REMOTE_FILES=1` leaves an `AnsiballZ_*.py` you can `explode` and `execute` on the host.

## Checked

Checked 2026-10-26 against ansible-core 2.21.5 sources and ansible-documentation main (2026-10-21); ansible-core 2.22 was at release candidate 1 (2026-10-13), so 2.22 behaviour is labelled as such.
- Confirmed: debugger values (`always`, `never`, `on_failed`, `on_unreachable`, `on_skipped`), `enable_task_debugger` / `ANSIBLE_ENABLE_TASK_DEBUGGER`, commands `p`, `task.args[...]`, `task_vars[...]`, `u`, `r`, `c`, `q`; `ANSIBLE_KEEP_REMOTE_FILES` plus `explode`; `--start-at-task`, `--step`, `--syntax-check`, `--list-tasks`, `--flush-cache`.
- Confirmed: `callback_result_format` / `ANSIBLE_CALLBACK_RESULT_FORMAT` choices `json` and `yaml`; ansible-core ships the callbacks default, junit, minimal, oneline and tree only, while `profile_tasks`, `timer` and `json` come from ansible.posix; `ANSIBLE_DEBUG` exists.
- Fixed: `p host.vars` is not a documented debugger command (`p host` is); the `json` stdout callback is not in ansible-core; the verbosity breakdown per level is replaced by the CLI help wording.
- Removed as unconfirmed: the AWX debugger remark and the exact error-message table rows.

Method: documentation only; no commands were run.
