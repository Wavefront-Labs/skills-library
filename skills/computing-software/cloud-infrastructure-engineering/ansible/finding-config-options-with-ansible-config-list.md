---
id: computing-software.cloud-infrastructure-engineering.ansible.finding-config-options-with-ansible-config-list
name: finding-config-options-with-ansible-config-list
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-cfg, ansible-config, config-option-lookup]
level: practitioner
status: docs-checked
description: "Find any setting's ini section/key, environment variable, default and type with ansible-config list and ansible-doc for plugin options."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/cli/ansible-config.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/cli/config.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Finding a config option's key, env var and default

Every setting can be set three ways (ini key, environment variable, sometimes a variable). Do not guess the names — query them.

## ansible-config list
```bash
ansible-config list | less                      # YAML: every core setting
ansible-config list | grep -B2 -A12 '^HOST_KEY_CHECKING:'
ansible-config list --format json                # or yaml (the default)
```
Each entry shows `default`, `description`, `env` (e.g. `ANSIBLE_FORKS`), `ini` (section + key, e.g. `[defaults] forks`), `type` and sometimes `vars` (inventory variable that overrides it).

## Plugin options
Connection, become, callback, inventory and other plugins carry their own options:
```bash
ansible-config list -t connection | grep -A15 'ssh:'      # -t: base, or a configurable plugin type
ansible-doc -t connection ansible.builtin.ssh             # shows ini/env/vars per option
ansible-doc -t callback ansible.posix.profile_tasks
```
Example: `ssh_args` is `[ssh_connection] ssh_args`, `ANSIBLE_SSH_ARGS`, var `ansible_ssh_args`.

## Generate a commented template
```bash
ansible-config init --disabled > ansible.cfg            # every setting commented out; --format is ini, env or vars
ansible-config init --disabled -t all > ansible.cfg      # include plugin settings
```

## Where is it currently set from?
```bash
ansible-config dump | grep -i forks        # shows value and origin, e.g. DEFAULT_FORKS(/srv/proj/ansible.cfg) = 20
```

## Gotchas
- Names in docs (`DEFAULT_FORKS`) are the internal key, not the ini key; always read the `ini:` block.
- Boolean env vars accept `true/false/yes/no/1/0`.

## Verify
- [ ] `ansible-config dump --only-changed` shows the setting with your file as origin.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in lib/ansible/cli/config.py: list (`--format` json or yaml), dump, view, init (`--format` ini/env/vars, `--disabled`), validate; `-t` choices all, base and the configurable plugin types.
- Confirmed in plugins/connection/ssh.py: ssh_args option with ini [ssh_connection] ssh_args, env ANSIBLE_SSH_ARGS and var ansible_ssh_args; config/base.yml DEFAULT_FORKS with env ANSIBLE_FORKS and ini [defaults] forks; booleans accept y/yes/on/1/true/t and n/no/off/0/false/f.
- Removed unconfirmed claims: plugin-type version gate and the jq filter.

Method: documentation only; no commands were run.
