---
id: computing-software.cloud-infrastructure-engineering.ansible.finding-always-changed-tasks-and-replacing-shell-with-modules
name: finding-always-changed-tasks-and-replacing-shell-with-modules
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, idempotency, changed-every-run, shell-to-module, command-instead-of-module]
level: practitioner
status: docs-checked
description: "Find tasks that report changed on every run and fix them by replacing shell and command with modules or adding creates, removes and changed_when."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html", "https://docs.ansible.com/projects/lint/rules/command-instead-of-module/", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/command_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Finding always-changed tasks and replacing shell

## Find them
```bash
ansible-playbook site.yml -l web01                 # first run converges
ansible-playbook site.yml -l web01 | tee run2.log  # second run should be changed=0
grep -E '^changed:' run2.log
ansible-lint -t no-changed-when,command-instead-of-module,command-instead-of-shell
```
Molecule's `idempotence` step automates the two-run test (not covered by the cited pages). `ansible-lint`'s `command-instead-of-module` rule recommends a dedicated module when one serves better (modules are more reliable, give clearer messages, and often support retries); its doc example is `apt-get update` via `command` replaced by `ansible.builtin.apt` with `update_cache: true`. A false positive can be silenced with `# noqa: command-instead-of-module` on the line. The page does not list every flagged command (see the rule source).

## Replace with modules
Illustrative mappings (judgement, not a list from the lint page):
| Shell habit | Module |
|---|---|
| `mkdir -p`, `chmod`, `chown`, `ln -s` | `ansible.builtin.file` |
| `sed -i`, `echo >>` | `lineinfile`, `blockinfile`, `replace` |
| `curl -o` / `wget` | `get_url` (with `checksum`) |
| `tar xzf` | `unarchive` |
| `systemctl enable --now` | `systemd_service` |
| `useradd`, `usermod -aG` | `user` (`append: true`) |
| `sysctl -w` | `ansible.posix.sysctl` |
| `firewall-cmd` | `ansible.posix.firewalld` |
| `git clone` | `git` |
| `yum install` | `dnf` |

## When a command is unavoidable
`ansible.builtin.command` is not run through a shell (`*`, `|`, `>`, `;`, `&` do not work; use `shell` for those). `creates` skips the task if a matching file exists (checked before `removes`); `removes` runs it only if a matching file exists. Check-mode support is partial: with `creates`/`removes` it reports correct changed status, otherwise the task is skipped. It returns no diff. The page does not say how changed status is decided in normal runs, so set it yourself.
```yaml
- name: Initialise database once
  ansible.builtin.command: /opt/app/bin/init-db
  args:
    creates: /var/lib/app/.initialised          # skip if the marker exists

- name: Read current version
  ansible.builtin.command: app --version
  register: ver
  changed_when: false                           # read-only
  check_mode: false                             # documented: forces the task to run under --check
```
Gate on `ansible_check_mode` (`when: not ansible_check_mode`) for tasks that cannot run in a simulation; registered-variable conditionals produce no output under check mode.

## Other always-changed causes (field experience, not in the pages)
- `service: state=restarted` outside handlers.
- Templates with timestamps or unordered dict output.
- `get_url` with `force: true`; `package: state=latest` while repos keep publishing.

## Verify
- [ ] Two consecutive runs: the second ends with `changed=0` for every host.

## Checked
Method: 2026-11-08 docs-only read of the Ansible check-mode page, the command module page and the ansible-lint command-instead-of-module rule (via its docs.ansible.com redirect). Confirmed creates/removes, partial check mode, no shell, check_mode: false, and the apt example. Removed profile_tasks callback line and the `when` example using stdout of an undefined variable; module-mapping table and other causes are flagged as experience, not sourced.
