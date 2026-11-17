---
id: computing-software.cloud-infrastructure-engineering.ansible.running-multiple-ansible-versions-side-by-side
name: running-multiple-ansible-versions-side-by-side
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, control-node, side-by-side-versions, multiple-venvs, python-venv]
level: practitioner
status: docs-checked
description: "Run several ansible-core versions side by side with per-project venvs, pipx suffixes, tox or EEs, and keep the right binary and collections on PATH."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/installation_guide/intro_installation.rst", "https://github.com/pypa/pipx/blob/main/src/pipx/main.py", "https://github.com/ansible/tox-ansible/blob/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Several Ansible versions side by side

Needed when one estate runs ansible-core 2.16 and another is on 2.18, or when testing an upgrade.

## Per-project venvs (simplest)
```bash
python3.11 -m venv ~/.venvs/ansible-216
~/.venvs/ansible-216/bin/pip install 'ansible-core>=2.16,<2.17'
python3.12 -m venv ~/.venvs/ansible-218
~/.venvs/ansible-218/bin/pip install 'ansible-core>=2.18,<2.19'
source ~/.venvs/ansible-218/bin/activate && ansible --version
```

## pipx with suffixes
```bash
pipx install --suffix=216 'ansible-core<2.17'
pipx install --suffix=218 'ansible-core<2.19'
ansible-playbook216 --version
```
The suffix is added to the end of each app name and to the virtual environment name; run `pipx list` to see the exposed binaries (for example `ansible-playbook216`).

## Matrix testing
- `tox-ansible` generates tox environments per Python and ansible-core version for collections, named like `integration-py3.12-devel`; run them with `tox --ansible -e <env>` or `tox --ansible -p auto`.

## Execution environments
One execution environment image per version avoids host Python and Ansible dependencies; `ansible-navigator` runs playbooks inside the image. Check the ansible-navigator documentation for the exact flag.

## Keep collections separate
A shared `~/.ansible/collections` can contain versions that need a newer core. Put collections per project (`collections_path = ./collections` in the project ansible.cfg) or per venv.

## Gotchas
- Check `which ansible` after activating a venv; a shell can remember the old path (`hash -r` clears it).
- Keep one venv per version rather than upgrading or downgrading in place.

## Verify
- [ ] `ansible --version` in each project shows the expected core, config file and Python path.

## Checked

Checked 2026-10-26 against the Ansible installation guide, the pipx source and the tox-ansible README (main). Confirmed: `pipx install ansible-core` and version pins; the pipx `--suffix` option (added to the end of app and virtual environment names); tox-ansible environment names such as `integration-py3.12-devel` and the `tox --ansible` invocation. Removed the Molecule remark and the unverified `ansible-navigator --eei` flag claim, and reworded the AAP remark.

Method: documentation only; no commands were run.
