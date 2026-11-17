---
id: computing-software.cloud-infrastructure-engineering.ansible.hiding-secrets-from-output-and-log-hygiene
name: hiding-secrets-from-output-and-log-hygiene
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, no-log-secrets, hide-sensitive-output, debug-secrets, log-path-hygiene, callback-plugins, job-output]
level: practitioner
status: docs-checked
description: "Keep secrets out of debug output, callback plugins, log_path files, diff output and controller job logs, and set retention and access controls on what is logged."
sources: ["Logging Ansible output (https://docs.ansible.com/ansible/latest/reference_appendices/logging.html)", "FAQ, keeping secret data (https://docs.ansible.com/ansible/latest/reference_appendices/faq.html)", "Masking secrets in Ansible output (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_secret_masking.html)", "Configuration settings, DEFAULT_NO_LOG, DEFAULT_NO_TARGET_SYSLOG, DISPLAY_ARGS_TO_STDOUT (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)", "Debugging modules, ANSIBLE_KEEP_REMOTE_FILES (https://docs.ansible.com/ansible/latest/dev_guide/debugging.html)", "ansible-core 2.22 porting guide (https://docs.ansible.com/ansible/latest/porting_guides/porting_guide_core_2.22.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hiding secrets from output, and log hygiene

## Where secrets leak (checklist)
| Leak path | Control |
|---|---|
| `debug: var=` / `msg:` with a secret | don't; print `secret | length` or a hash prefix instead (before ansible-core 2.22 `no_log` does not affect `debug` output) |
| registered results of tasks handling secrets | `no_log: true` on the task and any later debug |
| `--diff` of templates containing secrets | `diff: false` on that task |
| `-vvv` module invocation args | module-level `no_log` options, task `no_log` |
| `log_path` file | permissions, rotation, `no_log` |
| callback plugins (Splunk, Elastic, Slack...) | callbacks that write to files or external services must mask or skip `no_log` results themselves; from ansible-core 2.22 the task result they receive is masked |
| extra vars on the CLI | pass a vaulted file (`-e @vars.yml` with a vault id), never `-e password=...` |
| fact cache (jsonfile/redis) | do not `set_fact cacheable` secrets; protect cache dir |
| `ANSIBLE_KEEP_REMOTE_FILES=1` | keeps the remote module files, which carry the task arguments, on the target — avoid with secrets |

## Safe debugging of secret values
```yaml
- ansible.builtin.debug:
    msg: "token present={{ api_token is defined }}, length={{ api_token | default('') | length }}, sha256_prefix={{ (api_token | default('') | hash('sha256'))[:8] }}"
```
Enough to confirm the right secret was loaded without exposing it.

## log_path
```ini
[defaults]
log_path = /var/log/ansible/ansible.log
```
- Restrict the permissions of the log directory and file to the automation account, and rotate logs according to your retention policy.
- If you save Ansible output to a log you expose any secret data in that output; `no_log: True` hides the task's result. Treat the log as confidential.
- `no_target_syslog` defaults to `False`, which leaves Ansible logging to syslog on the target (and to the Windows Event Log for newer PowerShell modules); set it to `True` to disable that.

## From ansible-core 2.22: secret masking
ansible-core 2.22 (release candidate 1 on 2026-10-13; the latest release is 2.21.5) registers known secrets and replaces them with `$REDACTED$` on the screen, in the `log_path` file, in callback task results and in module logs on the managed node. Registered automatically: decrypted vault content, vault passwords, module options marked `no_log: true` by the module author, prompted passwords, plugin options marked `secret: true`, and values from the `password` and `unvault` lookups. Register your own value with the `register_secret` filter (for example `register: {api_token: _task.result.json.token | register_secret}`); `mask_secrets` redacts a string you write somewhere Ansible does not control. Limits from the docs: only the exact registered string is matched (an encoded or hashed copy is not masked), a very short secret is masked inside unrelated words, messages other Python libraries write to `log_path` through the standard `logging` module are not masked, and masking complements `no_log` rather than replacing it.

## Global no_log
`[defaults] no_log = True` (`ANSIBLE_NO_LOG`, default False) toggles Ansible's display and logging of task details for every task — useful for fully secret playbooks, painful to debug. Prefer per-task, as the docs recommend.

## Verify
- [ ] Run the playbook with known dummy secrets at `-vvv`, then search the log file and captured output for them: no matches.
- [ ] Log directory and cache permissions checked by a compliance task.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and ansible-core 2.21.5 / 2.22.0rc1 sources.
- Confirmed: `log_path` logs expose output secrets unless a task sets `no_log`; `no_log` does not affect debugging output before 2.22; `no_target_syslog` and `no_log` defaults and descriptions; `ANSIBLE_KEEP_REMOTE_FILES` keeps remote module files; the secret masking behaviour, automatic registrations and limits listed above (labelled as 2.22, which was a release candidate on the check date).
- Removed as unconfirmed: the Ansible controller (AWX or Automation Platform) retention, RBAC, credential masking and survey remarks, because their documentation is not in a public repository that was readable; the log directory mode, retention figure and umask remarks; the `grep` command.

Method: documentation only; no commands were run.
