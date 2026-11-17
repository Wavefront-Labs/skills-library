---
id: computing-software.cloud-infrastructure-engineering.ansible.default-groups-all-and-ungrouped
name: default-groups-all-and-ungrouped
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, inventory, static-inventory, all-group, ungrouped, default-groups, group-vars-all, implicit-groups, implicit-localhost, group-names, groups-magic-variable, inventory-hygiene, orphan-hosts]
level: practitioner
status: docs-checked
description: "Use the implicit all and ungrouped groups: global defaults in group_vars/all, and a CI check that fails when a host falls out of its groups into ungrouped."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_inventory.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/implicit_localhost.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/reference_appendices/special_variables.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/cli/inventory.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default groups: all and ungrouped

Every inventory has two groups you never have to declare:
- **all** contains every host. It is the parent of every other group.
- **ungrouped** contains the hosts that do not belong to any other group.

Every host belongs to at least two groups (`all` and `ungrouped`, or `all` and another group). The two groups are always present but can be implicit and may not appear in the inventory file.

```ini
mail.example.com              # top of the INI file, before any [group] header: ungrouped

[web]
web1.example.com
```
```bash
ansible-inventory --graph           # shows @all with its child groups, including @ungrouped
```

## 1. all as the place for global defaults
```
inventory/
  hosts.yml
  group_vars/
    all/
      main.yml        # ansible_user, ntp servers, proxy, timezone
      vault.yml       # encrypted org-wide secrets
```
Because `all` is the parent of every group, it has the **lowest** inventory precedence: a child group overrides its parent, and host variables override group variables. The documentation's advice is to set common defaults in a `group_vars/all` file. In a YAML inventory the same thing inline:
```yaml
all:
  vars:
    ansible_user: automation
  children:
    web: {hosts: {web1.example.com: {}}}
```
Targeting: `hosts: all` in a play, `ansible all -m ping`, `--limit 'all:!web'`.

## 2. ungrouped as a hygiene check
A host that drops out of its group (a typo in a group name, a forgotten line) lands in `ungrouped`, gets no variables from its intended group, and is skipped by every play that targets that group. Make that loud with a pre-flight play:
```yaml
- hosts: localhost
  gather_facts: false
  tasks:
    - ansible.builtin.assert:
        that: groups['ungrouped'] | default([]) | length == 0
        fail_msg: "Ungrouped hosts: {{ groups['ungrouped'] }}"
```
or inspect the group on the command line with `ansible-inventory -i inventory --graph ungrouped`.
Legitimately standalone hosts (a bastion, a monitoring box) should still get a real group (`[bastion]`) so they can carry `group_vars`.

## 3. Useful variables
- `groups['all']`, `groups['ungrouped']`: lists of host names (`groups` maps every inventory group to its hosts).
- `group_names`: the groups the current host is in; `'ungrouped' in group_names` flags a stray host from inside a play.
- `ansible_play_hosts_all`: all hosts targeted by the play.

## Gotchas
- The implicit `localhost` (created when you reference `localhost` and have not defined it) is not targetable with any group and is not part of `all`, so `hosts: all` does not run on the control node. It does use variables from `host_vars` and the `all` group. Defining `localhost` in inventory replaces the implicit one and makes it an ordinary host.
- Keep environment-specific values out of `group_vars/all`; put them in the environment's own group or inventory directory.

## Verify
- [ ] `ansible-inventory --graph` shows `@ungrouped:` empty (or containing only intended hosts).
- [ ] `ansible-inventory --host anyhost` shows a value from `group_vars/all` and a group override winning over it where expected.

## Checked
Date 2026-10-24. Documentation: the How to build your inventory page (default groups, child over parent precedence, `group_vars/all` advice), the Implicit localhost page, the Special variables page (`groups`, `group_names`, `ansible_play_hosts_all`) and `cli/inventory.py` (`--graph` takes a group name, `--host`). Removed the jq-based check, the sample graph output, and unconfirmed statements about per-source `ungrouped`, `all.yml` versus `all/` merging, and dynamic-plugin grouping.
Release: ansible-core 2.21.5 and the ansible-documentation main branch.
Method: documentation only; no commands were run.
