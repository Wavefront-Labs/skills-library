---
id: computing-software.cloud-infrastructure-engineering.ansible.project-local-collections-directory
name: project-local-collections-directory
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collections, project-collections, collections-dir, collections-path, playbook-adjacent-collections, awx-project-sync, requirements-yml]
level: practitioner
status: docs-checked
description: "Vendor or install collections into a playbook-adjacent collections/ directory so a project carries its own versions locally, in CI and in AWX project sync."
sources: ["Installing collections adjacent to playbooks (https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html)", "ansible-core COLLECTIONS_PATHS setting (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)", "AWX collections support (https://github.com/ansible/awx/blob/devel/docs/collections.md)", "AWX settings source, AWX_COLLECTIONS_ENABLED (https://github.com/ansible/awx/blob/devel/awx/main/conf.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project-local collections directory

Goal: each automation repo uses exactly the collection versions it was tested with, independent
of what is installed system-wide on a laptop, runner or controller.

## Layout
```
repo/
  ansible.cfg
  site.yml
  collections/
    requirements.yml
    ansible_collections/          # installed here, git-ignored (or vendored, see below)
      community/general/...
```
Ansible supports keeping collections adjacent to the playbook, in a `collections/ansible_collections/` directory next to it; this keeps all users of the project on the same versions, isolates the project from global installs and lets you version collections with the playbooks. Install into it:
```bash
ansible-galaxy collection install -r collections/requirements.yml -p ./collections
```
`-p ./collections` creates `./collections/ansible_collections/<ns>/<name>`.
Make it explicit for tools that do not start from the playbook dir (ansible-lint, ansible-doc,
ad-hoc commands):
```ini
# ansible.cfg
[defaults]
collections_path = ./collections:~/.ansible/collections:/usr/share/ansible/collections
```
The setting (`collections_path`, environment variable `ANSIBLE_COLLECTIONS_PATH`) is an ordered, colon-separated list of root paths; collections must be in nested `ansible_collections/<ns>/<name>` subdirectories. The default is `~/.ansible/collections:/usr/share/ansible/collections` (with `ANSIBLE_HOME` changing the first).

## Git-ignore or vendor?
- **Ignore** (`collections/ansible_collections/` in `.gitignore`) and install in CI/controller from `requirements.yml` — normal case.
- **Vendor** (commit the installed tree) only for air-gapped targets or patched forks; record why in the README and still keep `requirements.yml` for the versions.

## AWX / automation controller
If a project has `collections/requirements.yml`, project updates install it into a cache that is copied to the job's temporary directory before the job runs (setting "Enable Collection(s) Download", `AWX_COLLECTIONS_ENABLED`, default on). Galaxy credentials on the organization (in order) control which servers are used; with none defined, nothing is installed from requirements.yml for that organization's project updates. A `source:` on a requirement bypasses this.

## Gotchas
- If collections exist both in an EE image and in `collections/`, keep the versions aligned.
- `ansible-galaxy collection install` skips collections that are already installed; use `--upgrade` (newest version allowed) or `--force` (reinstall) in CI.
- Set `collections_path` in `ansible.cfg` explicitly for tools that do not start from the playbook directory.

## Verify
- [ ] `ansible-galaxy collection list -p ./collections` shows exactly the pinned versions.
- [ ] `ansible-config dump | grep COLLECTIONS_PATHS` shows the project path first.

## Checked

Checked 2026-10-26 against the Ansible collections guide (installing, adjacent-to-playbooks section), ansible-core `config/base.yml` (`COLLECTIONS_PATHS` default and nesting rule) and AWX (`docs/collections.md`, `AWX_COLLECTIONS_ENABLED` default true, Galaxy credential behaviour). Removed the unconfirmed lookup-precedence, plural setting name, vendoring and subdirectory claims.

Method: documentation only; no commands were run.
