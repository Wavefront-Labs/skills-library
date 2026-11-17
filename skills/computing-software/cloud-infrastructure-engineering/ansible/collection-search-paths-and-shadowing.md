---
id: computing-software.cloud-infrastructure-engineering.ansible.collection-search-paths-and-shadowing
name: collection-search-paths-and-shadowing
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collections-usage, ansible-collections-path, collection-shadowing, collections-path]
level: practitioner
status: docs-checked
description: "Control ANSIBLE_COLLECTIONS_PATH and collections_path order, detect duplicate collection versions shadowing each other, and find which copy Ansible loads."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths", "https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html#installing-collections-adjacent-to-playbooks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collection search paths and shadowing

## Search order
1. `collections/` next to the playbook (playbook-adjacent), searched before the configured paths.
2. `collections_path` from ansible.cfg / `ANSIBLE_COLLECTIONS_PATH` (colon-separated, left to right). Default: `ANSIBLE_HOME/collections:/usr/share/ansible/collections` (`ANSIBLE_HOME` is `~/.ansible` unless changed). Each entry is a root directory that must contain `ansible_collections/<namespace>/<name>`.
3. Any `ansible_collections` directory on Python's `sys.path`, appended after the configured paths; controlled by `collections_scan_sys_path` (default `true`).

The **first** location containing `ns.name` wins, regardless of version.

## Detect duplicates
```bash
ansible-galaxy collection list community.general
# <path-1>/ansible_collections   community.general <version-a>
# <path-2>/ansible_collections   community.general <version-b>
ansible-doc -F community.general              # plugin names with the source files actually used
ansible --version                             # includes the configured 'ansible collection location'
```
`ansible --version` prints only the configured `collections_path`, not `sys.path` entries.

## Typical shadowing bugs
- A project pins a collection version in `./collections`, but CI runs the playbook from a different directory and picks up another copy from the configured paths or `sys.path`.
- An older copy earlier in `collections_path` hides the version you just installed to a later entry.
- `ansible-galaxy collection install -p <dir>` into a path that is not on `collections_path`: galaxy warns (`collections_path_warning`, on by default since 2.16, not for a playbook-adjacent directory) and playbooks will not see it.

## Make it deterministic
```ini
[defaults]
collections_path = ./collections
collections_scan_sys_path = false     # ignore site-packages copies
```
(The ini key is `collections_path`; the environment variable is `ANSIBLE_COLLECTIONS_PATH`.)

## Gotchas
- With no `-p`, `ansible-galaxy collection install` writes to the first entry of `collections_path`.

## Verify
- [ ] `ansible-galaxy collection list` shows a single location per collection.

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) collections_guide/collections_installing.rst and the ansible-core devel sources (`config/base.yml`, `utils/collection_loader/_collection_finder.py`, `cli/galaxy.py`, `cli/doc.py`). Confirmed: the default `collections_path` value, the `collections_scan_sys_path` default, the playbook-adjacent then configured then `sys.path` order with first match winning, the galaxy path warning and its version, `ansible-doc -F` and the `--version` collection location line. Removed unconfirmed claims about the `ansible` package location, a duplicate-install warning, a deprecated `collections_paths` key, `ansible.builtin` and EE paths, and sample version numbers.
Method: documentation only; no commands were run.
