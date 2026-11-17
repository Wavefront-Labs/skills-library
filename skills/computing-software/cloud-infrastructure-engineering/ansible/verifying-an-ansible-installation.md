---
id: computing-software.cloud-infrastructure-engineering.ansible.verifying-an-ansible-installation
name: verifying-an-ansible-installation
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, control-node, install-verification, ansible-version-output]
level: intro
status: docs-checked
description: "Verify a fresh Ansible install: read ansible --version output, ping localhost and a managed node, and confirm config file, collections and Python in use."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/installation_guide/intro_installation.rst", "https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/arguments/option_helpers.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/__init__.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/config.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Verifying an Ansible installation

## Read ansible --version properly
```
ansible [core 2.17.4]
  config file = /srv/proj/ansible.cfg
  configured module search path = ['~/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = ~/.venvs/a/lib/python3.12/site-packages/ansible
  ansible collection location = ~/.ansible/collections:/usr/share/ansible/collections
  executable location = ~/.venvs/a/bin/ansible
  python version = 3.12.3 (main, ...) [GCC 13.2.0] (~/.venvs/a/bin/python3)
  jinja version = 3.1.4
  pyyaml version = 6.0.2 (with libyaml v0.2.6)
```
Check each line: `config file = None` means no ansible.cfg was found (or it was ignored for being in a world-writable dir). `pyyaml version = ... (without libyaml)` means the pure-Python YAML parser is in use, which is slower; install a PyYAML build with libyaml.

## Smoke tests
```bash
ansible localhost -m ansible.builtin.ping           # engine works without inventory
ansible localhost -m ansible.builtin.setup -a 'filter=ansible_distribution*'
ansible-galaxy collection list                      # collections visible
ansible-config dump --only-changed                  # which settings you actually changed
ansible all -i inventory -m ansible.builtin.ping -o # every managed node, one line each
ansible-community --version                         # version of the ansible package (not ansible-core)
```
"provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'" is a warning, not an error: no inventory configured.

## Typical failures
| Symptom | Cause |
|---|---|
| `ansible: command not found` after pipx | `~/.local/bin` not on PATH: `pipx ensurepath` |
| ping returns `UNREACHABLE` | SSH, not Ansible: try `ssh -v user@host` |
| ping `FAILED` with a missing-Python error | target Python missing or interpreter discovery picked the wrong one |
| module not found | collection not installed for this core/venv |

## Verify
- [ ] Version, config file and Python path match what the project expects.
- [ ] Managed-node ping returns `pong` for every host.

## Checked

Checked 2026-10-26 against the ansible-core source (devel) and the Ansible installation guide. Confirmed: the `ansible --version` lines (config file, configured module search path, ansible python module location, ansible collection location, executable location, python version, jinja version, and a `pyyaml version = ... (with libyaml ...)` line that replaced the old `libyaml` line); `ansible --version` shows the ansible-core version and `ansible-community --version` the ansible package; `ansible-config dump --only-changed`; the empty-host-list warning text; Ansible ignores an `ansible.cfg` in a world-writable directory; `pipx ensurepath`. Removed the exact `/usr/bin/python: not found` message.

Method: documentation only; no commands were run.
