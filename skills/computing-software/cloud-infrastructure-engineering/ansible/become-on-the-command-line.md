---
id: computing-software.cloud-infrastructure-engineering.ansible.become-on-the-command-line
name: become-on-the-command-line
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, become, become-cli, privilege-escalation, ad-hoc]
level: intro
status: docs-checked
description: "Use --become, -K, --become-user and --become-method on ad hoc and playbook runs, and know how CLI flags interact with play and inventory become settings."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_privilege_escalation.html", "https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/arguments/option_helpers.py", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# become on the command line

```bash
ansible web -m ansible.builtin.dnf -a 'name=httpd state=present' -b          # -b = --become
ansible web -m ansible.builtin.command -a 'id' -b --become-user postgres
ansible web -m ansible.builtin.shell -a 'whoami' -b -K                        # -K = --ask-become-pass
ansible web -m ansible.builtin.ping -b --become-method su -K
ansible-playbook site.yml -b -K
```

## Flags
| Flag | Meaning |
|---|---|
| `-b`, `--become` | run operations with become (no password implied) |
| `-K`, `--ask-become-pass` | ask for the become password; does not imply become; one password for all hosts |
| `--become-user USER` | default `root`; does not imply `--become` |
| `--become-method METHOD` | default sudo; others include su, pbrun, pfexec, doas, dzdo, ksu, runas, machinectl (`ansible-doc -t become -l` lists them) |
| `--become-password-file FILE` | read the password from a file; an executable file is run and its stdout used (ansible-core 2.12+) |

## Precedence
Order from lowest to highest: configuration settings, command-line options, playbook keywords,
variables, direct assignment. So `-b` overrides config but not a play or task `become: false`
keyword, and an inventory variable such as `ansible_become` or `ansible_become_user` overrides the
keywords too. Passing `-e ansible_become=true` (extra vars) overrides everything else.

To turn become off by default, leave `become` unset: the config option is `become` in
`[privilege_escalation]` (env `ANSIBLE_BECOME`, default false).

## Gotchas
- `-K` gives one password for all hosts; use `ansible_become_password` per host (from Vault) when the passwords differ.
- If the playbook seems to hang, it is probably stuck at the escalation prompt; stop it and rerun with `-K`.
- When both the login user and the target user are unprivileged, Ansible must make its temporary
  module file readable by the target user; see the unprivileged-user skill.

## Verify
```bash
ansible web -m ansible.builtin.command -a whoami -b -o      # root on every host
```

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_privilege_escalation.rst, general_precedence.rst)
and ansible-core devel sources (CLI option helpers, `config/base.yml`). Confirmed: flag names and meanings,
`--become-password-file` and its `version_added` 2.12, precedence categories, `become` ini/env names. Fixed:
the previous text said task keywords beat inventory variables, but variables outrank keywords. Removed an
unconfirmed `allow_world_readable_tmpfiles` claim and the "no `--no-become`" assertion.
Method: documentation only; no commands were run.
