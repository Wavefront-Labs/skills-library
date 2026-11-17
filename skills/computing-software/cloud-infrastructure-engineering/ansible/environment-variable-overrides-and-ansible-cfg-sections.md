---
id: computing-software.cloud-infrastructure-engineering.ansible.environment-variable-overrides-and-ansible-cfg-sections
name: environment-variable-overrides-and-ansible-cfg-sections
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-cfg, ansible-config, ansible-env-vars, environment-overrides, cfg-sections, ssh-connection-section, privilege-escalation-section, defaults-section, galaxy-section, inventory-section, ansible-config-list, ci-overrides]
level: practitioner
status: docs-checked
description: "Override any ansible.cfg setting with its ANSIBLE_* env var (found via ansible-config list) and put permanent settings in the right cfg section so they are read."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/cli/ansible-config.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/config/manager.py", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/config/base.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variable overrides and ansible.cfg sections

**Goal:** change one setting for one run (CI job, debugging session, a colleague's shell)
without editing the shared `ansible.cfg`, and put permanent settings in the right section so
they are actually read.

## 1. Find the variable for any setting
```bash
ansible-config list | grep -B2 -A12 '^HOST_KEY_CHECKING'
```
Each entry shows `env: - name: ANSIBLE_HOST_KEY_CHECKING` and `ini: - section: defaults, key: host_key_checking`.
Precedence per setting: **env var > ansible.cfg > default**. Env wins over every cfg file.

Common one-off overrides:
```bash
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook site.yml      # fresh lab hosts
ANSIBLE_CALLBACK_RESULT_FORMAT=yaml ansible-playbook site.yml    # readable results from the default callback
ANSIBLE_FORKS=50 ANSIBLE_PIPELINING=True ansible-playbook site.yml
ANSIBLE_KEEP_REMOTE_FILES=1 ANSIBLE_DEBUG=1 ansible-playbook site.yml -vvv
ANSIBLE_COLLECTIONS_PATH=./collections ansible-playbook site.yml
ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass ansible-playbook site.yml
ANSIBLE_INVENTORY=inventories/prod ansible-playbook site.yml
ANSIBLE_NOCOLOR=1 ANSIBLE_FORCE_COLOR=0 ...                     # CI logs
```
Booleans accept `True/False/yes/no/1/0`. Lists are comma separated (`ANSIBLE_CALLBACKS_ENABLED=ansible.posix.timer,ansible.posix.profile_tasks`).

## 2. Sections of ansible.cfg
```ini
[defaults]
inventory          = inventories/prod
remote_user        = automation
forks              = 25
interpreter_python = auto_silent
callback_result_format = yaml
callbacks_enabled  = ansible.posix.timer, ansible.posix.profile_tasks
roles_path         = roles:~/.ansible/roles
collections_path   = collections:~/.ansible/collections
host_key_checking  = True
retry_files_enabled = False
log_path           = ~/ansible.log

[privilege_escalation]
become        = True
become_method = sudo
become_user   = root
become_ask_pass = False

[ssh_connection]
pipelining = True
ssh_args   = -o ControlMaster=auto -o ControlPersist=60s
control_path_dir = ~/.ansible/cp
transfer_method = smart

[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml
cache = True
cache_plugin = jsonfile
cache_connection = ~/.ansible/inv_cache

[galaxy]
server_list = automation_hub, galaxy
[galaxy_server.automation_hub]
url   = https://hub.example.com/api/galaxy/content/published/
token = <token>

[colors]
changed = yellow
```
A key in the wrong section is not read; `ansible-config validate` reports unknown sections and keys. Some options accept several sections: the ssh `pipelining` option is read from `[defaults]`, `[connection]` or `[ssh_connection]`.

## 3. See what is actually in effect
```bash
ansible-config dump --only-changed          # every non-default setting and its origin
ansible-config dump --only-changed -t all   # include plugin settings (inventory, connection)
ansible-config view                         # prints the cfg file that was loaded
ansible-config init --disabled -t all > ansible.cfg.full   # every option, commented, as a template
```
The `origin` column shows `env: ANSIBLE_FORKS` vs `/path/ansible.cfg` — the fastest way to
explain "it works on my machine".

## Gotchas
- Plugin options (e.g. inventory plugin `cache`) have their own env names like `ANSIBLE_INVENTORY_CACHE`; `ansible-config list -t inventory` reveals them.
- The config file is the first readable of: `ANSIBLE_CONFIG` (a directory means `ansible.cfg` inside it), `ansible.cfg` in the current directory (skipped if that directory is world-writable), `~/.ansible.cfg`, `/etc/ansible/ansible.cfg`.
- Per-host connection behaviour belongs in inventory vars (`ansible_ssh_common_args`), not cfg; cfg applies to every host.

## Verify
- [ ] `ansible-config dump --only-changed` lists your override with origin `env:` while the variable is exported, and drops it when unset.
- [ ] After editing a section, `ansible-config dump --only-changed | grep <KEY>` shows the file path as origin.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in config/manager.py (stable-2.22): lookup order is CLI, variables, environment, then config file entries (env beats ini); config file search order and world-writable skip; ANSIBLE_CONFIG directory handling.
- Confirmed in config/base.yml and doc fragments: ANSIBLE_FORKS, ANSIBLE_HOST_KEY_CHECKING, ANSIBLE_KEEP_REMOTE_FILES, ANSIBLE_COLLECTIONS_PATH, ANSIBLE_INVENTORY_ENABLED (default host_list, script, auto, yaml, ini, toml), galaxy server_list ini key, callback result_format option (env ANSIBLE_CALLBACK_RESULT_FORMAT, ini callback_result_format), pipelining ini sections in the ssh plugin; core callbacks in 2.22 are default, junit, minimal, oneline and tree (no yaml stdout callback); boolean values y/yes/on/1/true/t and n/no/off/0/false/f.
- Removed unconfirmed claims: [persistent_connection] example, ansible-navigator and Controller remarks. Replaced the `yaml` stdout callback, which is not in ansible-core 2.22, with result_format.

Method: documentation only; no commands were run.
