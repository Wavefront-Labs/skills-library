---
id: computing-software.systems-network-administration.linux.ansible-ad-hoc-commands
name: ansible-ad-hoc-commands
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ansible, ansible-adhoc, ad-hoc-commands, ansible-command-module, ansible-shell, host-patterns, become, forks, fleet-operations, rhce, ex294, sysadmin]
level: practitioner
status: docs-checked
description: "Run one-off tasks across many Linux hosts with ansible ad-hoc commands: host patterns, command vs shell vs modules, become, forks and limits, check mode, and reading results."
sources:
  - https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html
  - https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html
  - https://docs.ansible.com/ansible/latest/cli/ansible.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ansible ad-hoc commands

**Goal:** answer or fix something on 200 hosts in one line — safely, idempotently where
possible — without writing a playbook.

## 1. Shape
`ansible <pattern> -i <inventory> -m <module> -a '<args>' [-b] [options]`
```bash
ansible all -m ping                                   # connectivity + Python, not ICMP
ansible web -m command -a 'uptime'                    # default module is command
ansible 'web:&prod:!web03' -a 'df -h /var'            # intersection and exclusion
ansible 'db*' --limit @retry_hosts.txt -a 'systemctl is-active postgresql'
ansible all --list-hosts -l 'site_ams'                # check what a pattern hits before acting
```

## 2. Pick the module
- `command` — no shell: pipes, `>`, `*` and `;` don't work (safer); environment variables are expanded by Ansible, not the shell.
- `shell` — needs pipes/redirects: `-m shell -a 'ss -ltn | grep -c :443'`.
- Real modules for changes — idempotent and report `changed`:
```bash
ansible web -b -m ansible.builtin.dnf -a 'name=openssl state=latest'
ansible web -b -m ansible.builtin.service -a 'name=nginx state=restarted'
ansible all -b -m ansible.builtin.user -a 'name=olduser state=absent remove=yes'
ansible all -b -m ansible.builtin.copy -a 'src=motd dest=/etc/motd mode=0644'
ansible all -b -m ansible.builtin.lineinfile -a 'path=/etc/ssh/sshd_config regexp=^PermitRootLogin line="PermitRootLogin no"'
ansible all -m ansible.builtin.setup -a 'filter=ansible_distribution*'    # facts
ansible all -b -m ansible.builtin.reboot -f 5                               # reboot 5 at a time, waits for return
```
`ansible-doc -s ansible.builtin.lineinfile` shows arguments.

## 3. Safety controls
- `-b` (become) only when needed; `-K` prompts for the sudo password.
- `--check --diff` with modules that support it — dry run before changing anything. `command`/`shell` only support check mode when `creates=` or `removes=` is given; otherwise the task is skipped.
- `-f N` forks (default 5) — raise for read-only queries, keep low for restarts.
- `-l`/`--limit` to canary hosts first; `-o` (one line per host) for readable output.
- `ansible ... -m shell -a 'cmd' | tee result.txt` keeps a copy of the output.

## 4. Reading output
`SUCCESS`/`CHANGED`, `FAILED`, `UNREACHABLE` (SSH/auth issue).
`rc`, `stdout`, `stderr` per host. For something you'll run twice, write a playbook.

## Gotchas
- `command`/`shell` cannot tell whether anything changed; use `creates=`/`removes=` to make them conditional.
- Quoting: wrap `-a` in single quotes; nested quotes for `lineinfile` lines get ugly — that's a playbook signal.
- Patterns with `!` need single quotes in bash.
- `ansible all -a 'rm ...'` hits every host in the inventory, including ones you forgot about — check `--list-hosts` first.

## Verify
- [ ] `ansible <pattern> --list-hosts` returns exactly the intended hosts before any change.
- [ ] A rerun of a module-based ad-hoc change reports `SUCCESS` (not `CHANGED`) on every host.

## Checked

2026-10-28

Confirmed: Ansible ad hoc guide (default module is command, default five forks, -f, -b, -K/--ask-become-pass, -C/--check, shell module for pipes), ansible CLI reference (--list-hosts, -l/--limit, -o/--one-line, -D/--diff), patterns guide (:&, :!, --limit @file), command module (creates/removes, check mode only with them, no shell operators), setup module (filter), user and reboot modules.

Removed or corrected: The claim that $VAR does not work in the command module (Ansible expands environment variables itself), that command/shell always report changed, that failed hosts are listed at the end of an ad-hoc run, and the colour mapping of results.

Method: documentation only; no commands were run.
