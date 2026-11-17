---
id: computing-software.cloud-infrastructure-engineering.ansible.shell-completion-and-running-ansible-from-source
name: shell-completion-and-running-ansible-from-source
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, control-node, argcomplete, shell-completion, bash-completion, zsh-completion, ansible-devel, source-install, git-checkout, pip-editable, env-setup, testing-prereleases]
level: practitioner
status: docs-checked
description: "Enable tab completion for ansible-* commands with argcomplete, and run ansible-core from a git checkout (devel or a release branch) to test fixes before they ship."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/installation_guide/intro_installation.rst", "https://github.com/ansible/ansible/blob/devel/hacking/env-setup", "https://kislyuk.github.io/argcomplete/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shell completion and running Ansible from source

## 1. Tab completion with argcomplete
Every `ansible-*` CLI is argcomplete-aware; only the shell hook is missing.
```bash
python3 -m pip install --user argcomplete           # or: pipx inject --include-apps ansible argcomplete
activate-global-python-argcomplete --user   # bash: writes ~/.bash_completion.d/python-argcomplete
# or per command, in ~/.bashrc:
eval "$(register-python-argcomplete ansible)"
eval "$(register-python-argcomplete ansible-playbook)"
eval "$(register-python-argcomplete ansible-galaxy)"
```
The Ansible guide describes bash (global completion needs bash 4.2; otherwise register each script) and notes limited support for zsh and tcsh, with a pointer to the argcomplete documentation for those shells.
Open a new shell, type `ansible-playbook --li<TAB>` and the matching options are offered.

## 2. Run ansible-core from a git checkout
Use this to reproduce a bug against `devel`, test a backport on a stable branch, or bisect.
```bash
git clone https://github.com/ansible/ansible.git ~/src/ansible
cd ~/src/ansible && git checkout stable-2.17        # or devel
python -m venv ~/.venvs/ansible-src && source ~/.venvs/ansible-src/bin/activate
pip install -r requirements.txt
source hacking/env-setup -q                          # puts bin/ and lib/ of the checkout on PATH and PYTHONPATH
ansible --version                                    # "ansible python module location" points into the checkout
```
The Ansible guide's recipe is to `source ./hacking/env-setup` (`env-setup.fish` for Fish; `-q` suppresses spurious warnings), install `requirements.txt`, and update with `git pull --rebase`; no installation step is needed. Collections are not in the checkout: install what you need with `ansible-galaxy collection install`.

## Gotchas
- Re-run `pip install -r requirements.txt` after `git pull` to pick up changed runtime dependencies.
- A source checkout on PATH shadows the packaged `ansible-core`; `which ansible` and `ansible --version` before blaming a bug on a release.
- `hacking/env-setup` affects only the shell that sourced it; CI must run it in the same step.

## Verify
- [ ] `ansible-playbook --<TAB><TAB>` lists options in a fresh shell.
- [ ] `ansible --version` reports a module location inside the checkout; `git log -1` in the checkout matches what you meant to test.

## Checked

Checked 2026-10-26 against the Ansible installation guide (documentation repository, devel). Confirmed: `argcomplete` installation with pip or `pipx inject --include-apps`; `activate-global-python-argcomplete --user` (bash 4.2 or later) and per-command `eval $(register-python-argcomplete ansible)`; limited zsh and tcsh support; running from a clone with `source ./hacking/env-setup` (`env-setup.fish`, `-q`), `python3 -m pip install --user -r ./requirements.txt` and `git pull --rebase`. Removed the editable-install step, fish and Ubuntu completion advice, the `--tags` remark and `pip check` advice, which the guide does not state. Removed the bisect example.

Method: documentation only; no commands were run.
