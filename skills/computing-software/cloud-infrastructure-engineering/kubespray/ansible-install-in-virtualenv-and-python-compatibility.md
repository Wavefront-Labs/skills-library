---
id: computing-software.cloud-infrastructure-engineering.kubespray.ansible-install-in-virtualenv-and-python-compatibility
name: ansible-install-in-virtualenv-and-python-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ansible, python, virtualenv, requirements, ansible-core]
level: intro
status: docs-checked
description: "Install Kubespray's pinned Ansible in a Python virtualenv with pip install -r requirements.txt and fix the no matching distribution error using the Python and ansible-core table."
sources:
  - https://kubespray.io/docs/ansible/ansible.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubespray pins its supported Ansible version in `requirements.txt`, and your Python version may limit which Ansible you can use. The recommended approach is a virtual environment:

```ShellSession
VENVDIR=kubespray-venv
KUBESPRAYDIR=kubespray
python3 -m venv $VENVDIR
source $VENVDIR/bin/activate
cd $KUBESPRAYDIR
pip install -r requirements.txt
```

If pip reports `Could not find a version that satisfies the requirement ansible==14.4.0` and `No matching distribution found`, your Python is not compatible with the Ansible version Kubespray supports. The page says Ansible 14 supports Python 3.12 through 3.14 on the control node.

Compatibility table from the page:

| ansible-core | Control node Python | Target node Python |
|---|---|---|
| >=2.21.0, <2.22.0 | 3.12-3.14 | 3.9-3.14 |

Use the table with the Python available on your Ansible host to decide which Ansible to use.

## Checked

2026-11-04. The venv commands, error text and compatibility table were confirmed on the Ansible page as it stands now.

Method: documentation only; no commands were run.
