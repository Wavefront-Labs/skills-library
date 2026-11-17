---
id: computing-software.cloud-infrastructure-engineering.ansible.troubleshooting-become-timeouts-and-sudo-password-errors
name: troubleshooting-become-timeouts-and-sudo-password-errors
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, become, become-timeout, missing-sudo-password, troubleshooting]
level: practitioner
status: docs-checked
description: "Diagnose become failures: Missing sudo password, Timeout waiting for privilege escalation prompt, incorrect password, sudo lecture and requiretty."
sources: ["Understanding privilege escalation (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_privilege_escalation.html)", "sudo become plugin source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/become/sudo.py)", "su become plugin source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/become/su.py)", "ssh connection plugin source (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/connection/ssh.py)", "Configuration settings, DEFAULT_TIMEOUT and pipelining (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting become failures

| Message | Cause | Fix |
|---|---|---|
| `Missing sudo password` | become needs a password, none supplied | `-K`, `ansible_become_password` from vault, or NOPASSWD |
| `Incorrect sudo password` | the become password was supplied but the become prompt reported a failure | check `ansible_become_password` or `-K` for the become method in use |
| `Timeout (12s) waiting for privilege escalation prompt` | the expected become prompt did not arrive within the wait (the connection `timeout` of 10 s plus 2 s) | find what delays or replaces the prompt; raise `timeout` only as a stopgap |
| sudo error about needing a tty | `requiretty` in `/etc/sudoers` conflicts with pipelining (the config docs say this is why pipelining is off by default) | remove `requiretty` or leave pipelining off |
| `Authentication failure` (su) | the su plugin matches this text (and `incorrect password` for BusyBox) as a failed password | check the password passed to su via `ansible_become_password` |

## Debug procedure
```bash
ansible host -m ansible.builtin.command -a id -b -vvvv
```
`-vvvv` prints the exact command Ansible wraps: `sudo -H -S -n -u root /bin/sh -c 'echo BECOME-SUCCESS-xxxx; ...'`. The default sudo `become_flags` are `-H -S -n`; when a become password is configured Ansible removes `-n` and adds `-p` with its own prompt text.

## Timeouts
While negotiating the prompt, the ssh plugin waits for the connection `timeout` plus 2 seconds. `timeout` defaults to 10 (`[defaults] timeout = 30` or `ANSIBLE_TIMEOUT`), which is where `Timeout (12s)` comes from. Fix whatever delays the prompt; raise the timeout only as a stopgap.

## Prompt detection
When a become password is set, Ansible injects its own prompt with `sudo -p "[sudo via ansible, key=...] password:"` and waits for exactly that text, so a prompt produced by some other mechanism (for example an MFA module) is not recognised and ends in the timeout above. The su plugin matches a list of localised `Password` prompts instead.

## Verify
- [ ] `ansible all -b -m ansible.builtin.command -a 'id -u'` returns 0 everywhere.

## Checked

Checked 2026-10-26 against ansible-core 2.21.5 sources (devel, 2026-10-23) and ansible-documentation main (2026-10-21).
- Confirmed in `ssh.py`: the messages `Missing <method> password`, `Incorrect <method> password` and `Timeout (%ds) waiting for privilege escalation prompt`, with the wait equal to 2 plus the connection `timeout` (default 10, so 12 s).
- Confirmed in the sudo plugin: default `become_flags` `-H -S -n`, `-n` removed and `-p "[sudo via ansible, key=...] password:"` added when a password is set, `BECOME-SUCCESS-<id>` marker; su plugin `fail` strings and localised prompt list; the `requiretty` and pipelining conflict from the `pipelining` setting description.
- Removed as unconfirmed: sudo's own message texts for sudoers and tty errors, the claim about which user's password sudo asks for, `passprompt_override`, PAM and SSSD timing remarks, and the ssh/sudo test commands.

Method: documentation only; no commands were run.
