---
id: computing-software.cloud-infrastructure-engineering.ansible.ad-hoc-file-transfer-facts-packages-and-services
name: ad-hoc-file-transfer-facts-packages-and-services
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ad-hoc, adhoc, ad-hoc-copy, ad-hoc-file, ad-hoc-facts, setup-filter, facts-filter, ad-hoc-service, ad-hoc-package, ad-hoc-user, fetch, copy, setup-module, service-module, package-module, fleet-queries, one-liners, key-value-args]
level: practitioner
status: docs-checked
description: "Push/pull files with copy and fetch, gather one fact fleet-wide with setup filter=, install packages, restart services and manage users from a single ansible -m line."
sources: ["https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/setup_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/setup.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/fetch.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/arguments/option_helpers.py", "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/callback/json.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ad hoc file transfer, facts, packages and services

Syntax: `ansible <pattern> -m <module> -a "<key=value ...>" [-b] [-f N] [--limit]`.
Arguments are `key=value` pairs; quote the whole `-a` string, and quote values containing
spaces with single quotes inside: `-a "content='hello world' dest=/tmp/x"`.
Complex args (lists, dicts) can be JSON: `-a '{"name": ["git","vim"], "state": "present"}'`.

## 1. Files
```bash
ansible web -m ansible.builtin.copy -a "src=./motd dest=/etc/motd owner=root mode=0644" -b
ansible web -m ansible.builtin.copy -a "content='maintenance tonight' dest=/etc/motd" -b
ansible web -m ansible.builtin.file -a "path=/var/app/cache state=absent" -b
ansible web -m ansible.builtin.file -a "path=/opt/app state=directory owner=app mode=0750" -b
ansible all -m ansible.builtin.fetch -a "src=/etc/ssh/sshd_config dest=./collected/ flat=no"
# fetch appends <hostname>/<path> to dest unless flat=yes; with flat=yes a dest ending in / uses the source basename
ansible db -m ansible.builtin.lineinfile -a "path=/etc/hosts line='10.0.0.5 vip' regexp='vip$'" -b
```
Every run reports `CHANGED` or `SUCCESS` per host, so a second identical copy shows
`SUCCESS` — ad hoc commands are as idempotent as the module.

## 2. Facts across a fleet
```bash
ansible all -m ansible.builtin.setup -a "filter=ansible_distribution*"      # shell glob on fact names
ansible all -m ansible.builtin.setup -a "filter=ansible_default_ipv4"
ansible all -m ansible.builtin.setup -a "gather_subset=!all,!min,hardware filter=ansible_memtotal_mb"
ansible all -m ansible.builtin.setup --tree /tmp/facts        # --tree (-t): log output to this directory
```
`filter` takes shell-style (fnmatch) patterns and a list since 2.11; it filters only the first-level subkey below `ansible_facts`.

## 3. Packages, services, users
```bash
ansible web -m ansible.builtin.package -a "name=htop state=present" -b
ansible web -m ansible.builtin.dnf -a "name=* state=latest" -b -f 20            # -f sets the fork count (default 5)
ansible web -m ansible.builtin.apt -a "update_cache=yes upgrade=dist" -b
ansible web -m ansible.builtin.service -a "name=nginx state=restarted" -b
ansible web -m ansible.builtin.systemd_service -a "name=nginx state=reloaded daemon_reload=yes" -b
ansible all -m ansible.builtin.service_facts -b
ansible all -m ansible.builtin.user -a "name=jdoe state=absent remove=yes" -b    # offboarding
```
Use `-f 1` or `--limit` to limit how many hosts act at once when restarting services on a load-balanced pool.

## 4. Capture output
```bash
ANSIBLE_STDOUT_CALLBACK=ansible.posix.json ansible all -m setup -a filter=ansible_kernel > kernels.json
ANSIBLE_STDOUT_CALLBACK=oneline ansible all -m command -a uptime
ansible all -m command -a "df -h /" --one-line
```

## Gotchas
- The default module of the `ansible` command is `command`, whose `-a` value is a free-form command (the docs reboot example is `ansible atlanta -a "/sbin/reboot" -f 10`); other modules take key=value pairs.
- Quote the whole `-a` string so the shell does not mangle it; for complex arguments write a playbook.
- `fetch` with `flat=yes` and several hosts writes every host's file to the same `dest`, so each overwrites the last.
- `setup filter=` matches first-level fact names only (`ansible_eth0` yes, `ansible_eth0.ipv4` no).
- The `json` stdout callback is not in ansible-core; it is `ansible.posix.json`.

## Verify
- [ ] `ansible web -m copy -a "src=./motd dest=/etc/motd" -b` twice: first `CHANGED`, second `SUCCESS`.
- [ ] The `setup` filter output lists `ansible_kernel` for every host.

## Checked
Checked 2026-10-26 against ansible-documentation `intro_adhoc.rst`, ansible-core devel `setup.py`, `fetch.py`,
`option_helpers.py` (`-f`, `-o/--one-line`, `-t/--tree`), the callback plugin directory (`oneline` builtin; `json` in
ansible.posix). Confirmed: `command` default module and free-form args, fork count, `filter` first-level semantics and list
type since 2.11, `gather_subset` form, `fetch flat` behaviour. Corrected: `json` callback is `ansible.posix.json`. Removed
unconfirmed claims: error message text, sudo-password behaviour, ad hoc lacking `serial`, the `jq` pipeline and the lookup-based
`authorized_key` one-liner.
Method: documentation only; no commands were run.
