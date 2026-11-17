---
id: computing-software.cloud-infrastructure-engineering.ansible.secrets-in-registered-results-diffs-and-censored-output
name: secrets-in-registered-results-diffs-and-censored-output
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, no-log-secrets, censored-output, register-secrets, diff-false, no-log]
level: practitioner
status: docs-checked
description: "Stop secrets leaking through registered results, --diff output and debug of censored values; know what no_log hides and the censored placeholder."
sources: ["Logging Ansible output (https://docs.ansible.com/ansible/latest/reference_appendices/logging.html)", "Validating tasks: diff mode and diff: false (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html)", "FAQ, keeping secret data (https://docs.ansible.com/ansible/latest/reference_appendices/faq.html)", "Masking secrets in Ansible output (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_secret_masking.html)", "Task execution source, censored result text (https://github.com/ansible/ansible/blob/devel/lib/ansible/_internal/_task.py)", "ansible-core 2.22 porting guide (https://docs.ansible.com/ansible/latest/porting_guides/porting_guide_core_2.22.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Secrets in registers, diffs and censored output

## What no_log does
```yaml
- name: Fetch DB password
  ansible.builtin.command: vault kv get -field=password kv/app
  register: db_pw
  changed_when: false
  no_log: true
```
Output becomes:
`ok: [app01] => {"censored": "the output has been hidden due to the fact that 'no_log: true' was specified for this result"}`
- The **registered variable still contains the secret** in memory; any later `debug: var=db_pw` prints it.
- The censored result is what is displayed and passed on; the registered variable is not censored.

## Leak paths and fixes
| Leak | Fix |
|---|---|
| `debug: var=db_pw` later | do not debug secrets; debug `db_pw.stdout | length` |
| Using `db_pw.stdout` in a module without no_log | `no_log: true` on every task that consumes it |
| `--diff` on template/copy/lineinfile showing the secret line | `diff: false` on the task (or block) |
| Loop label printing the item | `loop_control: {label: "{{ item.name }}"}` plus no_log |
| Module option marked `no_log` by its author | before ansible-core 2.22 the value is replaced by `VALUE_SPECIFIED_IN_NO_LOG_PARAMETER` in the result; from 2.22 the real value stays in the result and is masked in output |
| `set_fact` with secret, fact caching enabled | `cacheable: false`; the `jsonfile` cache writes plain JSON |

## diff: false
```yaml
- name: Render app secrets file
  ansible.builtin.template:
    src: secrets.env.j2
    dest: /etc/app/secrets.env
    mode: "0600"
  diff: false
  no_log: true
```
The docs note that `--diff` can reveal sensitive information and show `diff: false` as the way to disable it for a task.

## Global safety net
`[defaults] no_log` (`ANSIBLE_NO_LOG`) defaults to False; `no_log: true` at play level hides everything and makes the play hard to debug. Prefer task or block scope.

## From ansible-core 2.22: secret masking
ansible-core 2.22 (release candidate 1 on 2026-10-13; the latest release is 2.21.5) registers known secrets and replaces them with `$REDACTED$` on the screen, in the `log_path` file, in callback task results and in module logs on the managed node. Registered automatically: decrypted vault content, vault passwords, module options marked `no_log: true` by the module author, prompted passwords, plugin options marked `secret: true`, and values from the `password` and `unvault` lookups. Register your own value with the `register_secret` filter (for example `register: {api_token: _task.result.json.token | register_secret}`); `mask_secrets` redacts a string you write somewhere Ansible does not control. Limits from the docs: only the exact registered string is matched (an encoded or hashed copy is not masked), a very short secret is masked inside unrelated words, messages other Python libraries write to `log_path` through the standard `logging` module are not masked, and masking complements `no_log` rather than replacing it.

The 2.22 docs show the safest pattern for a generated value: keep `no_log: true` on the producing task and register the value with a projection such as `register: {db_password: _task.result.stdout | register_secret, password_result: _task.result}`, so later `debug` output shows `$REDACTED$`.

## Verify
Run the play with `--diff -v` using a known dummy secret and search the captured output for it; there must be no match.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5 / 2.22.0rc1 sources.
- Confirmed: the censored result text with its `censored` key; `no_log` hides the task's result while a registered variable still holds the value (a later `debug` prints it before 2.22); `diff: false`; `loop_control` `label`; `ANSIBLE_NO_LOG`; the `VALUE_SPECIFIED_IN_NO_LOG_PARAMETER` change and the `register_secret` pattern in 2.22 (a release candidate on the check date).
- Removed as unconfirmed: controller job-event and `-vvvv` remarks, the claim that `no_log` hides failure messages for debugging purposes, and the shell grep.

Method: documentation only; no commands were run.
