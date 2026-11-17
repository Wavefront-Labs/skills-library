---
id: computing-software.cloud-infrastructure-engineering.ansible.molecule-inside-collections-extensions-layout
name: molecule-inside-collections-extensions-layout
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, molecule, molecule-collection-layout, extensions-molecule, collection-testing, ansible-creator, role-in-collection]
level: advanced
status: docs-checked
description: "Run Molecule scenarios for roles and playbooks inside a collection using the extensions/molecule layout, shared config, FQCN role references and collection-aware paths."
sources: ["Molecule collections guide (https://github.com/ansible/molecule/blob/main/docs/getting-started-collections.md)", "Molecule configuration, nested scenarios (https://github.com/ansible/molecule/blob/main/docs/configuration.md)", "Collection structure, extensions directory (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Molecule inside collections (extensions/molecule)

Goal: test the roles and playbooks shipped in a collection with Molecule, from the collection
root, against the collection's own code (not a stale installed copy).

## Layout
```
ansible_collections/acme/platform/
  galaxy.yml
  roles/webserver/...
  extensions/
    molecule/
      config.yml                    # shared base config for all scenarios
      webserver_default/
        molecule.yml
        converge.yml
        verify.yml
      integration_hello/
        molecule.yml
        converge.yml
```
`ansible-creator init collection acme.platform` scaffolds a collection with an `extensions/molecule` directory. Molecule finds scenarios under `extensions/molecule/` when run from the collection root; `molecule list` shows them. The `extensions` directory holds content that extends the collection beyond the standard plugins and roles.

## Shared config
`extensions/molecule/config.yml` is the base config that scenarios inherit: it holds what every scenario repeats (for example `ansible.executor.args` pointing at a shared inventory, `scenario.test_sequence`, `shared_state`). Each scenario's `molecule.yml` holds only overrides; an empty `molecule.yml` inherits everything. With `shared_state: true` the `default` scenario handles create and destroy for all scenarios.

## converge.yml uses FQCN
```yaml
- name: Converge
  hosts: all
  gather_facts: true
  tasks:
    - ansible.builtin.include_role:
        name: acme.platform.webserver
```
The role is referenced by FQCN, so the collection must be findable on the collections path, for example by working from a checkout located at `.../ansible_collections/acme/platform` or by installing the working copy:
```bash
ansible-galaxy collection install . --force -p ~/.ansible/collections   # before molecule runs, in CI
```

## Run
```bash
cd ansible_collections/acme/platform
molecule test --all              # every scenario found in extensions/molecule/
molecule test -s webserver_default
```
Nested scenario directories are supported: target them with `-s group/scenario` (or `-s "group/*"`), and set `MOLECULE_GLOB="extensions/molecule/**/molecule.yml"` so `molecule list` and `--all` discover them.

## Gotchas
- Make sure the FQCN resolves to the working copy and not an older installed version; check with `ansible-galaxy collection list acme.platform`.
- `ansible-test integration` targets and Molecule scenarios overlap; use ansible-test for modules/plugins, Molecule for roles/playbooks.

## Verify
- [ ] `molecule list` from the collection root lists all scenarios.
- [ ] A deliberate change in `roles/webserver` makes the corresponding scenario fail (proves it tests the working copy).

## Checked

Checked 2026-10-26 against Molecule main (`docs/getting-started-collections.md`, `docs/configuration.md` nested scenarios) and the Ansible collection structure documentation. Confirmed: `ansible-creator init collection`, `extensions/molecule/config.yml` as inherited base config, `shared_state`, `molecule test --all` and `-s`, nested scenarios with `MOLECULE_GLOB`, FQCN `include_role`. Removed unconfirmed version gate, dependency step, silent-older-version and `build_ignore` claims.

Method: documentation only; no commands were run.
