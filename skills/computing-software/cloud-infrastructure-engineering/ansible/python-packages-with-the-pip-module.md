---
id: computing-software.cloud-infrastructure-engineering.ansible.python-packages-with-the-pip-module
name: python-packages-with-the-pip-module
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, packages-repos, pip-module, virtualenv, python-venv]
level: practitioner
status: docs-checked
description: "Install Python packages on targets with ansible.builtin.pip into virtualenvs, pin versions and requirements files, avoid PEP 668 externally-managed errors and system pip."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/pip_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/pip.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Python packages with the pip module

## Into a virtualenv (recommended)
```yaml
- name: Ensure venv tooling
  ansible.builtin.package:
    name: [python3, python3-pip]          # package names vary by distribution

- name: Install app requirements into a venv
  ansible.builtin.pip:
    requirements: /opt/app/requirements.txt
    virtualenv: /opt/app/venv
    virtualenv_command: python3 -m venv
  become: true
  become_user: app

- name: Pin a single package
  ansible.builtin.pip:
    name: gunicorn==22.0.0
    virtualenv: /opt/app/venv
```
`virtualenv_command` is the command used to create the environment (default `virtualenv`; the docs list `pyvenv` as an example).
`virtualenv_python` should not be used when `virtualenv_command` is `pyvenv` or the `-m venv` module.

## System Python and PEP 668
Python installations marked externally managed (PEP 668) cannot be modified by pip 23.0.1 and later without
`break_system_packages` (module docs; option added in 2.17). Options:
1. Use a venv (above).
2. Use the distribution's package for the library.
3. Last resort: `break_system_packages: true` on the task.

## Options
| Option | Use |
|---|---|
| `state` | present, latest, absent, forcereinstall |
| `executable` | specific pip, e.g. `pip3.11` |
| `extra_args` | extra arguments passed to `pip` |
| `chdir` | directory to change to before running pip |
| `umask` | umask applied while installing |

## Modules that need Python libs on the target
Install them into the interpreter Ansible uses (`ansible_python_interpreter`), e.g. `psycopg2` for community.postgresql: pip into a venv and set `ansible_python_interpreter: /opt/ansible-venv/bin/python` for that host, or use the distro package.

## Gotchas
- `state: latest` moves to a newer release whenever one is published, so pin versions where reproducibility matters.
- Pass index credentials through `environment` with `no_log: true` rather than in task output.

## Verify
- [ ] The venv's `pip freeze` on the host lists the pinned versions.

## Checked
Checked 2026-10-26 against ansible-core devel `pip.py` documentation block. Confirmed: `requirements`, `virtualenv`,
`virtualenv_command` (default `virtualenv`), `virtualenv_python` restriction, `state` choices (present, latest, absent,
forcereinstall), `executable`, `extra_args`, `chdir`, `umask`, and `break_system_packages` (2.17) with the PEP 668 note.
Corrected: the skill suggested `extra_args: --break-system-packages`; the module has a dedicated option. Removed unconfirmed
distribution version list, example `extra_args` flags, Debian package name, and idempotence-with-extras claim.
Method: documentation only; no commands were run.
