---
id: computing-software.cloud-infrastructure-engineering.ansible.display-skipped-hosts-and-task-args-output
name: display-skipped-hosts-and-task-args-output
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, debugging, display-skipped-hosts, display-args, callback-plugins]
level: intro
status: docs-checked
description: "Tune default callback output: hide skipped and ok hosts, show task arguments in headers, enable check mode markers and result formats for readable logs."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/default_callback.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html#display-args-to-stdout", "https://docs.ansible.com/ansible/latest/plugins/callback.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Output tuning for the default callback

```ini
[defaults]
stdout_callback = ansible.builtin.default
callback_result_format = yaml        # multi-line yaml results; default json (since 2.13)
display_skipped_hosts = False        # hide "skipping:" lines (default True)
display_ok_hosts = True              # default True
display_failed_stderr = True         # failures to stderr (default False)
show_task_path_on_failure = True     # print the task path on failure (default False)
check_mode_markers = True            # [CHECK MODE] tags in output (default False)
show_custom_stats = True             # print set_stats data at the end (default False)
display_args_to_stdout = False       # see below (default False)
```
Env equivalents: `ANSIBLE_DISPLAY_SKIPPED_HOSTS=false`, `ANSIBLE_CALLBACK_RESULT_FORMAT=yaml`, `ANSIBLE_DISPLAY_ARGS_TO_STDOUT=true`.

## display_args_to_stdout
When true, task headers include the arguments after the task name, comma separated: `TASK [<name> path=/srv/app, state=directory]`. Helpful for many tasks that use the same action; **risky** if args contain secrets, so secure stdout or set `no_log: true` on those tasks (the default callback leaves the arguments out of the header for `no_log` tasks). Keep it false in shared logs.

## Choosing other callbacks
| Need | Callback |
|---|---|
| very terse | `community.general.dense` or `ansible.builtin.minimal` |
| JSON for tooling | `ansible.posix.json` (or `ansible.posix.jsonl`) |
| timings | `callbacks_enabled = ansible.posix.profile_tasks, ansible.posix.timer` |

## Per run
```bash
ANSIBLE_DISPLAY_SKIPPED_HOSTS=false ANSIBLE_CALLBACK_RESULT_FORMAT=yaml ansible-playbook site.yml -v
```

## Gotchas
- `display_skipped_hosts = False` also hides skipped *items* in loops (the default callback checks the same option for items); confusing when debugging conditionals.
- `callback_result_format` (`json` or `yaml`) applies to callbacks that use the result-format options, including `default`; `callback_result_indentation` (default 4) and `callback_format_pretty` tune it.
- Non-core callbacks such as `profile_tasks` and `timer` must be listed in `callbacks_enabled`.

## Verify
- [ ] A run with conditionals shows no `skipping:` lines and multi-line YAML results.

## Checked
Checked 2026-10-25 against ansible-core devel `plugins/callback/default.py`, `plugins/doc_fragments/default_callback.py` and `result_format_callback.py`, `config/base.yml` (DISPLAY_ARGS_TO_STDOUT, CALLBACKS_ENABLED), plus the ansible.posix and community.general callback listings on GitHub (commit of 2026-10). Confirmed: option names, environment names and defaults, the header format of `display_args_to_stdout` and that `no_log` suppresses it, skipped items hidden by `display_skipped_hosts`, `callback_result_format` choices (since 2.13), and the callback names in the table. Corrected the claim that `no_log` does not hide headers; removed unconfirmed claims about AWX behaviour and the replaced `yaml` callback.
Method: documentation only; no commands were run.
