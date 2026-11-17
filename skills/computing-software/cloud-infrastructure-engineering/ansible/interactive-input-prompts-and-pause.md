---
id: computing-software.cloud-infrastructure-engineering.ansible.interactive-input-prompts-and-pause
name: interactive-input-prompts-and-pause
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, vars-prompt, pause, interactive-input, prompts, confirmation, private-input, encrypt-password-hash, confirm, unsafe-input, extra-vars, non-interactive, ci-safe, maintenance-windows, human-gate]
level: practitioner
status: docs-checked
description: "Take human input in Ansible safely: vars_prompt with private/encrypt/confirm, pause for approval gates and timed waits, and how to keep the same playbook runnable non-interactively in CI and AWX."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_prompts.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/pause_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interactive input: vars_prompt and pause

**Goal:** the few runs that genuinely need a human (a one-off password, a go/no-go on
prod) ask clearly, hide secrets, and still work when a scheduler or CI runs the same
playbook with no terminal.

## 1. `vars_prompt`
```yaml
- hosts: db
  vars_prompt:
    - name: release_tag
      prompt: "Release tag to deploy"
      private: false
      default: "1.0"                # overridable default
    - name: db_admin_password
      prompt: "DB admin password"
      private: true                 # no echo (default)
      confirm: true                 # ask twice
      encrypt: sha512_crypt         # hash the entered value
      salt_size: 7                  # default salt size is 8
    - name: approve
      prompt: "Type PROD to continue"
      private: false
      unsafe: true                  # do not template the typed value
  pre_tasks:
    - ansible.builtin.assert:
        that: approve == 'PROD'
        fail_msg: "Aborted by operator"
```
Rules:
- A prompt is **skipped** for any variable already defined with `--extra-vars` (`-e name=value`), and when running from a non-interactive session such as cron or AWX; this is how CI runs the same play.
- `encrypt` hashes the value so it can be used with the `user` module's `password`. With Passlib installed any scheme it supports works (only `salt` or `salt_size` are accepted as parameters); without it Ansible falls back to the Python `crypt` library and supports at most `bcrypt`, `md5_crypt`, `sha256_crypt` and `sha512_crypt`, depending on the platform.
- `unsafe: true` for anything an operator may type containing `{{` or `{%`.
- `private: false` is required for visible input; the default hides it. Since ansible-core 2.22 a value entered for a private prompt is also registered as a secret and masked in output.

## 2. `pause`
```yaml
- ansible.builtin.pause:
    prompt: "Canary looks healthy? Press Enter to continue, Ctrl-C then A to abort"
  run_once: true
  when: not (auto_approve | default(false) | bool)

- ansible.builtin.pause: {seconds: 30}         # fixed wait (replication lag, LB drain)
- ansible.builtin.pause: {minutes: 2, prompt: "Waiting for cache warm-up"}
- ansible.builtin.pause:
    prompt: "Enter OTP"
    echo: false
  register: otp
  run_once: true
```
- A `pause` with a prompt and no timer waits until the prompt is acknowledged (Ctrl-C then `C` continues, then `A` aborts the playbook). Gate it with a variable (`auto_approve`) as above for unattended runs.
- Prompting for a set amount of time is not supported: with `seconds` or `minutes`, `prompt` is only a message, and no input is captured or echoed. A zero or negative value waits 1 second.
- The module bypasses the host loop, and with `serial` you are prompted once per batch; `run_once: true` is harmless.
- The typed value is returned as `user_input` (only when no timer is set); `echo: false` hides typing (default true).
- For a per-host wait use `wait_for`, not `pause`.

## 3. Choosing
| Situation | Tool |
|---|---|
| Value known before the run | `-e`, `--extra-vars @file.yml`, AWX survey |
| Secret that must not sit on disk | `vars_prompt private`, or `--ask-vault-pass`/vault client |
| Human go/no-go in a rolling update | `pause` + `run_once`, between `serial` batches |
| Wait for an external system | `until`/`retries` on a check task, not a blind `pause` |
| Scheduled, unattended | none; `-e auto_approve=true` and no prompts |

## Gotchas
- `vars_prompt` is a play keyword, so it belongs on the play, not in a role or task file.
- Special characters such as `{` and `%` in a prompted value can cause templating errors; set `unsafe: true` to accept them.
- Typed passwords are not stored in a vault; use `no_log: true` on the tasks that use them.

## Verify
- [ ] Running with `-e release_tag=v1.2.3 -e auto_approve=true -e db_admin_password=...` completes with zero prompts (CI mode).
- [ ] Running interactively hides the password characters and rejects a mismatched confirmation.

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_prompts.rst and the ansible-core devel `pause` module documentation. Confirmed: `private`, `confirm`, `encrypt`, `salt_size` (default 8), `unsafe`, skipping of prompts for extra-vars and non-interactive sessions, Passlib versus `crypt` scheme support, `pause` options, `user_input`, per-batch prompting with `serial`, Ctrl-C behaviour, and the 2.22 masking note (devel docs). Removed unconfirmed claims about prompt timing, AWX survey conversion, stdin piping, TTY behaviour in controller jobs and the git-based default.
Method: documentation only; no commands were run.
