---
id: computing-software.cloud-infrastructure-engineering.ansible.collections-keyword-in-plays-and-roles
name: collections-keyword-in-plays-and-roles
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collections, collections-keyword, fqcn, collection-search-path, meta-main, short-names, ansible-lint]
level: practitioner
status: docs-checked
description: "Use the collections keyword in plays and role meta/main.yml to resolve short module names, know what it does not cover, and why FQCN is still the recommended default."
sources: ["https://docs.ansible.com/ansible/latest/collections_guide/collections_using_playbooks.html", "https://ansible.readthedocs.io/projects/lint/rules/fqcn/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The `collections` keyword in plays and roles

Goal: understand how Ansible resolves a short name like `firewalld:` and control it explicitly,
so a module from the wrong collection never runs silently.

## In a play
```yaml
- hosts: web
  collections:
    - ansible.posix
    - community.general
  tasks:
    - firewalld: {service: https, permanent: true, immediate: true, state: enabled}   # -> ansible.posix.firewalld
```
The `collections` keyword only creates an ordered search path for unqualified module, action plugin and role names. You do not need to list `ansible.builtin`: standard ansible-core content and support for older third-party plugin paths stay available by default.

## In a role
The play's list is **not** inherited by roles. A role declares its own in `meta/main.yml`:
```yaml
collections:
  - community.mysql
dependencies: []
```
Roles inside a collection automatically search their own collection first.

## What it does not affect
- Only unqualified module and action plugin names (and role references) in that play or role.
- Not other plugin types: lookups, filters and tests (for example in `{{ }}` templates) still need an FQCN such as `community.general.json_query`.
- It does not install anything; the collection must be present (`ansible-galaxy collection list`).

## Recommendation
The docs recommend an FQCN over the `collections` keyword (`ansible.posix.firewalld`). ansible-lint's `fqcn` rule enforces it (`fqcn[action]`, `fqcn[action-core]`), flags the keyword itself as `fqcn[keyword]`, and can be fixed automatically with `--fix`; it does not take the keyword into account when resolving names. Reserve the keyword for:
- legacy roles being migrated in steps, or
- making a set of short names explicit in generated/test playbooks.

## Gotchas
- Two collections that ship the same module name: the list is an ordered search path, so order decides; an FQCN removes the ambiguity.
- Roles called from a play do not inherit the play's `collections`, even when the role has no `meta/main.yml` list of its own.
- Playbooks shipped in a collection (`ansible-playbook namespace.collection.playbook`, since 2.11) get an implied entry for their own collection, like roles in a collection.

## Verify
- [ ] Each short name used under `collections:` resolves to the intended collection (use FQCNs in a test play to compare).
- [ ] `ansible-lint` reports no `fqcn[action-core]`, `fqcn[action]` or `fqcn[keyword]` after migration.

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) collections_guide/collections_using_playbooks.rst and the ansible-lint `fqcn` rule page. Confirmed: roles do not inherit the play's list, role `meta/main.yml` list wins, roles in a collection search their own collection first, the keyword only builds a search path (FQCN still needed for lookups, filters and tests), `ansible.builtin` need not be listed, and the lint rule names and `--fix`. Removed unconfirmed claims about the exact legacy/builtin search order, `library/` shadowing, `ansible-doc` resolution and grep-based verification; corrected the claim that role names need an FQCN.
Method: documentation only; no commands were run.
