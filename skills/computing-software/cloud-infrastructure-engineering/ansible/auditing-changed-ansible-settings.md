---
id: computing-software.cloud-infrastructure-engineering.ansible.auditing-changed-ansible-settings
name: auditing-changed-ansible-settings
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-cfg, only-changed, config-validate, config-dump]
level: practitioner
status: docs-checked
description: "Audit effective Ansible configuration with ansible-config dump --only-changed and validate, catch unknown keys, typos and deprecated settings before they bite."
sources: ["https://docs.ansible.com/ansible/latest/cli/ansible-config.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/cli/config.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Auditing changed settings

## What differs from defaults, and where from
```bash
ansible-config dump --only-changed
# DEFAULT_FORKS(/srv/proj/ansible.cfg) = 30
# HOST_KEY_CHECKING(env: ANSIBLE_HOST_KEY_CHECKING) = False
ansible-config dump --only-changed -t all       # explicit form; 2.22 defaults -t to all (-t base = base settings only)
ansible-config dump --format json --only-changed > effective-config.json
```
The origin in parentheses tells you whether a value comes from the file, an env var or the default — the fastest way to find a stray `ANSIBLE_*` variable in a CI image.

## Validate the file
```bash
ansible-config validate                         # checks the config file (and ANSIBLE_ variables) for unknown sections/keys
ansible-config validate -c ansible.cfg --format ini     # --format is ini or env
```
A typo like `[defualts]` or `host_key_check = False` is otherwise silently ignored.

## Deprecated settings
Current names to use: `[defaults] callbacks_enabled` (since 2.11) and `[defaults] collections_path` (since 2.10); neither the old `callback_whitelist` nor `collections_paths` spellings appear in the 2.22 settings definitions. Settings that are deprecated carry a `deprecated:` block in `ansible-config list`.

## Diff two environments
```bash
ANSIBLE_CONFIG=ci/ansible.cfg ansible-config dump --only-changed > ci.txt
ansible-config dump --only-changed > local.txt
diff local.txt ci.txt
```

## Gotchas
- `dump` shows the config of the Ansible you ran it with, so run it inside the same environment (venv or container) as your playbooks.
- Environment variables override the file silently; CI images often set `ANSIBLE_FORCE_COLOR`.

## Verify
- [ ] `ansible-config validate` exits 0 and `--only-changed` contains only intended settings.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in lib/ansible/cli/config.py (stable-2.22): subcommands list, dump, view, init, validate; `dump --only-changed` (alias `--changed-only`), `--format` choices json/yaml/display for dump, ini/env for validate, `-c/--config`, `-t` default all with base as previous behaviour.
- Confirmed in config/manager.py that environment variables override ini entries and the origin is recorded as env: or the file path; in config/base.yml that callbacks_enabled (2.11) and collections_path (2.10) are the current ini keys.
- Removed unconfirmed claims: the 2.14 version gate for validate, deprecation-warning wording, ansible-navigator remark.

Method: documentation only; no commands were run.
