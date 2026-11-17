---
id: computing-software.cloud-infrastructure-engineering.ansible.control-node-setup-and-upgrades
name: control-node-setup-and-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, control-node, ansible-install, ansible-core, pipx, pip, ansible-community-package, version-pinning, python-version, ansible-cfg, ansible-config, config-precedence, collections-path, upgrade, interpreter-python, config-locations, config-dump, world-writable]
level: practitioner
status: docs-checked
description: "Install an Ansible control node with pipx, pick ansible-core or the community package, match Python to the core version, and know the ansible.cfg search order and precedence."
sources: ["https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html", "https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html", "https://docs.ansible.com/ansible/latest/cli/ansible-config.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Control node setup and upgrades

**Goal:** a control node (laptop, bastion, CI runner) whose Ansible version is pinned,
isolated from the OS Python, and reproducible on the next machine.

## 1. Pick the package
- `ansible-core`: the engine plus `ansible.builtin`; you add collections yourself.
- `ansible` (community package): `ansible-core` plus a curated set of collections (the release page says "more than 85").
- `ansible --version` reports the core version; `ansible-community --version` reports the community package version.

Control node: a UNIX-like system (Windows only via WSL). Managed nodes need Python but not Ansible; network modules are an exception, as they run on the control node.

## 2. Match Python to the core version
Control-node Python versions from the support matrix:

| ansible-core | Control node Python | Community package |
|---|---|---|
| 2.21 | 3.12-3.14 | 14.x |
| 2.20 | 3.12-3.14 | 13.x |
| 2.19 | 3.11-3.13 | 12.x |
| 2.18 | 3.11-3.13 | 11.x |
| 2.17 | 3.10-3.12 | 10.x (end of life) |
| 2.16 | 3.10-3.12 | |
| 2.15 | 3.9-3.11 | |

ansible-core maintains the latest release plus the two before it, with patch releases roughly every four weeks. Check the matrix before upgrading the OS Python or choosing a pin; re-read it, as it moves with each release.

## 3. Install with pipx
```bash
pipx install --include-deps ansible            # community package
pipx install ansible-core==<version>           # or core only, pinned
pipx upgrade --include-injected ansible        # upgrade, including injected packages
pipx inject ansible argcomplete                # add a package to the same venv
```
pip is the other documented route (`pip install --user ...`).

## 4. ansible.cfg: search order and precedence
First file found wins, the rest are ignored: `ANSIBLE_CONFIG` (env var) then `./ansible.cfg` (cwd), then `~/.ansible.cfg`, then `/etc/ansible/ansible.cfg`. A cwd `ansible.cfg` in a world-writable directory is not loaded automatically (the config page documents this; it does not say whether a warning appears).

Precedence, lowest to highest: configuration settings (ansible.cfg, then environment variables, which override the file), command-line options, playbook keywords, variables, direct assignment. So `ANSIBLE_FORKS` beats the file, and `-e` extra vars override everything the command line otherwise sets (the page calls this a variable, not an option).

Settings that matter on a new node (names and defaults from the config page):

| Setting | ini key / env var | Default |
|---|---|---|
| forks | `[defaults] forks` / `ANSIBLE_FORKS` | 5 |
| host key checking | `host_key_checking` / `ANSIBLE_HOST_KEY_CHECKING` | True |
| interpreter | `interpreter_python` / `ANSIBLE_PYTHON_INTERPRETER` | `auto` (other mode: `auto_silent`, which drops the warning on fallback) |
| pipelining | `pipelining` (under `[connection]` or `[defaults]`) / `ANSIBLE_PIPELINING` | False |
| collections | `collections_path` / `ANSIBLE_COLLECTIONS_PATH` | |
| roles | `roles_path` / `ANSIBLE_ROLES_PATH` | |
| inventory | `inventory` / `ANSIBLE_INVENTORY` | |
| become method | `[privilege_escalation] become_method` | sudo |

Pipelining conflicts with privilege escalation: with `sudo` you must first disable `requiretty` on the managed hosts, which is why it is off by default.

Inspect settings with `ansible-config`: `dump` (add `--only-changed` for values that differ from the default), `view` (the config file in use), `list`, `init` (add `--disabled` to comment every entry out, e.g. `ansible-config init --disabled > ansible.cfg`; `-t all` includes plugin settings), `validate`. `-c <CONFIG_FILE>` points at a specific file.

## 5. Upgrading
1. Read the support matrix for the new core version and confirm the control-node Python is in range.
2. Upgrade with `pipx upgrade --include-injected ansible`, or reinstall with a new pin.
3. Re-run `ansible --version` to confirm the core version, Python and config file, then run your playbooks in check mode before rollout.

## Gotchas
- `ansible --version` also reports the config file location; if it is not the file you expect, an earlier entry in the search order is winning.
- Ten-series community packages (`ansible` 10.x, core 2.17) are end of life; do not pin them in new work.

## Verify
- [ ] `ansible --version` shows the pinned core version.
- [ ] `ansible-config dump --only-changed` lists exactly the settings you intended.

## Checked
Date: 2026-11-07. Read in full: the Installing Ansible page and the ansible-core support matrix; the configuration-file section and the entries for forks, host_key_checking, interpreter_python, pipelining (page lists `[connection]` and `[defaults]`), collections_path, roles_path, become_method and inventory on the configuration settings page (searched, not every entry read); the precedence page's categories and config section; the ansible-config CLI page's action list and `--only-changed`, `--disabled`, `-c`, `-t` options. The `become_method` default is as read; the `[privilege_escalation]` section name was not re-confirmed on the page.
Corrected: "core 2.17+ drops Python 3.9" was wrong (2.16 already requires 3.10-3.12; 3.9 is listed only for 2.15); `ansible==10.*` pins an end-of-life release; "silently, with a warning" for a world-writable directory is not on the page; `auto` is not documented as warning on each host, only on the fallback.
Removed as not on a cited page: `pipx inject ansible ansible-lint molecule`, the "~100 collections" count, the RHEL `dnf install ansible-core` note and "never sudo pip" advice, venv and `pip freeze` recipes, `ansible-galaxy collection list` lockfile, porting-guide path, the `callback_result_format` and `[ssh_connection] pipelining` lines, `become = True`, the `pip install ansible` plus core mismatch claim, and the RHCE bare-title source.
Method: documentation only; no commands were run.
