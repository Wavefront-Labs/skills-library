---
id: computing-software.cloud-infrastructure-engineering.ansible.limiting-runs-to-host-list-and-retry-files
name: limiting-runs-to-host-list-and-retry-files
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, host-patterns, limit-file, retry-files, limit, rerun-failed-hosts]
level: practitioner
status: docs-checked
description: "Re-run a playbook only on hosts that failed, or on a list from a ticket, using --limit @file and retry files, including enabling and locating .retry output."
sources: ["https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html#patterns-and-ansible-playbook-flags", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html#retry-files-enabled", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/config/base.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Limiting runs to a host-list file or retry file

## --limit @file
`--limit @path` reads the list of hosts from a file:
```bash
printf 'web3.example.com\ndb7.example.com\n' > /tmp/ticket-4711.hosts
ansible-playbook site.yml --limit @/tmp/ticket-4711.hosts --list-hosts
ansible-playbook site.yml --limit @/tmp/ticket-4711.hosts
```
Check `--list-hosts` first to confirm which hosts the file actually selects.

## Retry files
Retry files are **off by default** (`RETRY_FILES_ENABLED` is False). Turn them on per project:
```ini
# ansible.cfg
[defaults]
retry_files_enabled = True
retry_files_save_path = ./.retry      # directory for .retry files
```
or `ANSIBLE_RETRY_FILES_ENABLED=1`. After a run Ansible writes `<playbook-name>.retry` listing the failed hosts from all plays; the file is overwritten each time. Re-run only them:
```bash
ansible-playbook site.yml --limit @.retry/site.retry
```
Add `.retry/` and `*.retry` to `.gitignore`.

## Without retry files
Copy the failed and unreachable hosts from the PLAY RECAP into a file (one name per line) and pass it with `--limit @failed.hosts`.

## Gotchas
- The retry file is overwritten on each run; a second partial failure shrinks it — keep the first copy if you need the full failure set.

## Verify
- [ ] `--list-hosts` with the file shows exactly the failed set.
- [ ] Second run recap shows those hosts `failed=0 unreachable=0`.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/inventory_guide/intro_patterns.rst: `--limit @file` reads hosts from a file, `.retry` file created when RETRY_FILES_ENABLED is true, lists failed hosts from all plays, overwritten on every run, `--limit @site.retry`.
- Confirmed in config/base.yml: RETRY_FILES_ENABLED default False (env ANSIBLE_RETRY_FILES_ENABLED), RETRY_FILES_SAVE_PATH (env ANSIBLE_RETRY_FILES_SAVE_PATH, default unset).
- Removed unconfirmed claims: 2.8 version gate, the "Could not match" warning, default save location, unreachable hosts in retry files, the JSON-callback recipe (core 2.22 has no json callback), fact and delegation remarks, AWX relaunch remark.

Method: documentation only; no commands were run.
