---
id: computing-software.cloud-infrastructure-engineering.ansible.per-project-ansible-cfg-and-relative-paths
name: per-project-ansible-cfg-and-relative-paths
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-cfg, per-project-cfg, relative-config-paths, project-layout]
level: practitioner
status: docs-checked
description: "Keep a per-project ansible.cfg next to playbooks, resolve relative paths for inventory, roles and collections, and avoid the world-writable-dir trap."
sources: ["https://docs.ansible.com/projects/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/projects/ansible/latest/installation_guide/intro_configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Per-project ansible.cfg

Ansible uses the first of: `$ANSIBLE_CONFIG`, `./ansible.cfg`, `~/.ansible.cfg`, `/etc/ansible/ansible.cfg`. No merging: the first file found wins entirely. Commit a project ansible.cfg so every engineer and CI gets the same behaviour.

```ini
# <project>/ansible.cfg
[defaults]
inventory = inventories/prod/hosts.yml
roles_path = roles:~/.ansible/roles
collections_path = collections
remote_user = automation
interpreter_python = auto_silent
stdout_callback = ansible.builtin.default
retry_files_enabled = false

[ssh_connection]
pipelining = true
```

## Relative paths
For many options a relative path is resolved **relative to the ansible.cfg file in use**, not the current directory; the `{{CWD}}` macro gives a path relative to the working directory, which the docs do not recommend. The `./ansible.cfg` lookup itself only finds a file in the directory you run from, so point `ANSIBLE_CONFIG` at the file to run from elsewhere.

## Running from elsewhere
```bash
ANSIBLE_CONFIG=/srv/proj/ansible.cfg ansible-playbook /srv/proj/site.yml
```
In CI, `cd` into the project root first.

## World-writable trap
If the current directory is world-writable (Vagrant shared folders, `/mnt/c` under WSL, some CI workspaces), Ansible does not automatically load `./ansible.cfg` from it (a security measure). Restrict access to the directory, or set `ANSIBLE_CONFIG` explicitly.

## Gotchas
- `~/.ansible.cfg` on a laptop silently stops applying once a project cfg exists: settings you relied on (e.g. `host_key_checking`) vanish.
- Do not put secrets (vault passwords) in the cfg; point `vault_password_file` at a script or file outside git.

## Verify
- [ ] `ansible --version` shows `config file = <project>/ansible.cfg`.
- [ ] `ansible-inventory --graph` works from the project root without `-i`.

## Checked
2026-10-28. Confirmed against Ansible docs "Ansible Configuration Settings" (config file search order, first file found wins, world-writable directory rule, relative-path rule and `{{CWD}}` macro), the `base.yml` config definitions (`interpreter_python` values, `retry_files_enabled`, `stdout_callback`) and `option_helpers.py` (`ansible --version` prints `config file =`). Removed: `callback_result_format` (not in the config reference), the list of specific path settings, and the quoted warning text (not in the docs).
Method: documentation only; no commands were run.
