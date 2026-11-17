---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-builtin-module-index-by-category
name: ansible-builtin-module-index-by-category
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, modules-fqcn, builtin-modules, modules, fqcn]
level: intro
status: docs-checked
description: "Navigate the ansible.builtin module index by job (files, packages, services, commands, utilities, net) and pick the right builtin before reaching for a collection."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ansible.builtin modules by category

`ansible.builtin` is the collection of core modules. Use the fully qualified name (`ansible.builtin.copy`) in tasks.

| Job | Modules |
|---|---|
| Files | `copy`, `template`, `file`, `lineinfile`, `blockinfile`, `replace`, `stat`, `find`, `fetch`, `slurp`, `assemble`, `tempfile`, `unarchive`, `get_url` |
| Packages | `package`, `dnf`, `dnf5`, `yum_repository`, `rpm_key`, `apt`, `apt_key`, `apt_repository`, `deb822_repository`, `pip` |
| Services | `service`, `systemd_service`, `sysvinit`, `service_facts`, `package_facts` |
| Users | `user`, `group`, `getent` |
| Commands | `command`, `shell`, `raw`, `script`, `expect` |
| System | `hostname`, `reboot`, `cron`, `known_hosts`, `mount_facts`, `setup`, `gather_facts` |
| Network/HTTP | `uri`, `get_url`, `wait_for`, `wait_for_connection`, `iptables` |
| Flow/utility | `debug`, `assert`, `fail`, `set_fact`, `set_stats`, `include_vars`, `include_tasks`, `import_tasks`, `include_role`, `import_role`, `import_playbook`, `add_host`, `group_by`, `meta`, `pause`, `async_status`, `validate_argument_spec` |
| SCM | `git`, `subversion` |

Modules that are not in this list (for example `firewalld`, `mount`, `ufw`, `parted`) are not in `ansible.builtin`: look them up in the collection index for the other collections before assuming they are available.

## Verify
- [ ] Every module a play uses appears in the builtin index, or comes from a collection you have installed.

## Checked
2026-11-01. Every module name in the table was confirmed in the ansible.builtin collection index page (modules and their one-line descriptions); `yum` is not listed there. Removed: the list of modules said to live in ansible.posix and community.general, the `ansible-doc` commands, the `ansible.legacy` shadowing note, the `yum` removal version, the `systemd` alias, the `mount_facts` version gate and the ansible-lint rule name, none of which that page states.
Method: documentation only; no commands were run.
