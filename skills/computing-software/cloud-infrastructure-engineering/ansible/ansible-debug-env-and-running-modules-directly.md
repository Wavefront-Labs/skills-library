---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-debug-env-and-running-modules-directly
name: ansible-debug-env-and-running-modules-directly
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, debugging, ansible-debug-env, keep-remote-files, module-development]
level: advanced
status: docs-checked
description: "Debug Ansible internals with ANSIBLE_DEBUG, keep and execute the generated module payload on the target, and run modules directly with args files."
sources: ["https://docs.ansible.com/ansible/latest/dev_guide/debugging.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ANSIBLE_DEBUG and running modules directly

## ANSIBLE_DEBUG
```bash
ANSIBLE_DEBUG=1 ansible-playbook site.yml -l web01 2>&1 | tee debug.log
```
Turns on Ansible's internal debug output (config setting `DEFAULT_DEBUG`, env `ANSIBLE_DEBUG`, default off). Very noisy; treat the log as sensitive and use it on a test host only. It is separate from `-vvvv`, which adds connection and command detail.

## Keep the module payload on the target
```bash
ANSIBLE_KEEP_REMOTE_FILES=1 ansible web01 -m ansible.builtin.dnf -a 'name=nginx' -b -vvv
```
The `-vvv` output shows the remote temp path, for example `~/.ansible/tmp/ansible-tmp-<id>/AnsiballZ_dnf.py`. Pipelining is disabled while `ANSIBLE_KEEP_REMOTE_FILES` is on.

On the target:
```bash
cd ~/.ansible/tmp/ansible-tmp-<id>/
python3 AnsiballZ_dnf.py explode        # unpacks to debug_dir/ with the module source and args
vi debug_dir/ansible/modules/dnf.py     # add prints
python3 AnsiballZ_dnf.py execute        # run the exploded module with the args file
```
The `args` file in `debug_dir` holds the JSON arguments Ansible passed; edit it to change the parameters. `execute` puts `debug_dir` first on `sys.path`.

## Gotchas
- Delete kept temp dirs afterwards: they contain the module arguments, possibly secrets.
- Modules with extra Python dependencies (for example `requests`) need those installed where you run the exploded module; Ansible bundles only `ansible.module_utils` imports.

## Verify
- [ ] Executing the exploded module reproduces the failure seen in the play.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/dev_guide/debugging.rst: ANSIBLE_KEEP_REMOTE_FILES=1 with -vvv shows the temp path, `explode` creates debug_dir, `args` file, `execute` runs with it and prepends debug_dir to sys.path.
- Confirmed in config/base.yml: DEFAULT_DEBUG env ANSIBLE_DEBUG; DEFAULT_KEEP_REMOTE_FILES env ANSIBLE_KEEP_REMOTE_FILES; ANSIBLE_PIPELINING is disabled when keep remote files is on.
- Removed unconfirmed claims: the run-a-module-directly recipe, action-plugin remark, PID/timestamp description of ANSIBLE_DEBUG.

Method: documentation only; no commands were run.
