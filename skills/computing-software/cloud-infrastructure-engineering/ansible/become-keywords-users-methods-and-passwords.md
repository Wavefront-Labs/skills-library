---
id: computing-software.cloud-infrastructure-engineering.ansible.become-keywords-users-methods-and-passwords
name: become-keywords-users-methods-and-passwords
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, become, privilege-escalation, become-user, become-method, become-password, ask-become-pass, ansible-become-password, become-flags, sudo, su, play-level-become, task-level-become, become-exe]
level: practitioner
status: docs-checked
description: "Set become, become_user, become_method and become_flags at play, block, task or inventory level, supply become passwords with --ask-become-pass or ansible_become_password, and read the sudo errors."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_privilege_escalation.html", "https://docs.ansible.com/ansible/latest/plugins/become.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/sudo_become.html", "https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/connection/ssh.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# become keywords, users, methods and passwords

## 1. The keywords and where they go
| Keyword | Meaning | Inventory/variable form |
|---|---|---|
| `become: true` | escalate | `ansible_become` |
| `become_user: postgres` | target user (default `root`); does not imply `become: true` | `ansible_become_user` |
| `become_method: sudo` | become plugin (sudo is the default) | `ansible_become_method` |
| `become_flags: '-H -S -n'` | extra flags to the method (sudo default `-H -S -n`) | `ansible_become_flags` |
| `become_exe: /usr/local/bin/sudo` | executable (sudo plugin option, also a keyword) | `ansible_become_exe` |

Keywords inherit play, then block/role, then task, and the most specific wins. Variables (such as
`ansible_become` set in inventory) override playbook keywords, which in turn override command-line
options and configuration (config < command line < keywords < variables < direct assignment).
```yaml
- hosts: db
  become: true                      # whole play as root
  tasks:
    - name: Run as the postgres user only here
      community.postgresql.postgresql_db:
        name: app
      become_user: postgres
    - name: Back to the login user
      ansible.builtin.command: id
      become: false
```
Valid `become_method` values listed in the docs: sudo, su, pbrun, pfexec, doas, dzdo, ksu,
runas, machinectl (and `enable` for network devices). `ansible-doc -t become -l` lists the
installed plugins. The sudo plugin's default flags are `-H -S -n`; when a become password is
supplied, Ansible drops `-n` from the flags so sudo can read the password.

## 2. Passwords
```bash
ansible-playbook site.yml -K                 # --ask-become-pass: one password for all hosts
ansible-playbook site.yml -k -K              # ssh password and become password
ansible-playbook site.yml --become-password-file ./pw.sh   # core 2.12+; an executable file is run and its stdout used
```
Per host or group, keep it in a vaulted variable:
```yaml
# group_vars/legacy/vault.yml (ansible-vault encrypt)
ansible_become_password: "{{ vault_become_password }}"
```
`ansible_become_pass` is accepted as an alias. `-K` does not itself turn become on. If a playbook
that uses become seems to hang, it is probably waiting at the privilege escalation prompt; stop it
and rerun with `-K`.

## 3. Reading the errors
| Message | Meaning |
|---|---|
| `Missing sudo password` | sudo asked for a password and none was supplied (the sudo plugin matches `sudo: a password is required`); use `-K`, `ansible_become_password` or NOPASSWD |
| `Incorrect sudo password` | sudo answered `Sorry, try again.` |
| `Timeout (Ns) waiting for privilege escalation prompt` | raised by the ssh connection plugin when the expected prompt did not appear in time |

## 4. Check what will run
`ansible-playbook -vvv` prints the connection and the become wrapper command;
`ansible host -m command -a whoami -b` is the one-line test.

## Gotchas
- `become_user` without `become: true` does nothing: it does not imply become.
- A play-level `become: true` also applies to tasks delegated to localhost, which then try to
  escalate on the control node; set `become: false` on those tasks (unless an inventory variable
  `ansible_become` overrides it).
- Privilege escalation cannot be limited to specific commands: Ansible runs modules from temporary
  files whose names change, so a sudoers rule that allows only named command paths will fail.
- Methods cannot be chained (no `sudo /bin/su -`).

## Verify
- [ ] `ansible all -b -m command -a whoami` returns `root` on every host; with `--become-user svc` it returns `svc`.

## Checked
Checked 2026-10-23 against ansible-documentation (playbooks_privilege_escalation.rst, general_precedence.rst)
and ansible-core devel sources (sudo become plugin, ssh connection plugin, `config/base.yml`, CLI option
helpers; devel is 2.23 dev). Confirmed: keyword and variable names, sudo flag default and `-n` removal when a
password is set, the method list, `--become-password-file` (`version_added` 2.12), error strings, precedence
order, no command-level restriction. Removed unconfirmed claims about `requiretty` as a cause of
`Incorrect sudo password`, `su` password ownership, sudoers messages, host-versus-`-K` precedence and CI hangs.
Method: documentation only; no commands were run.
