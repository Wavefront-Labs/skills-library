---
id: computing-software.cloud-infrastructure-engineering.ansible.scaffolding-and-versioning-a-collection
name: scaffolding-and-versioning-a-collection
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collection-development, collection-init, collection-versioning, semver, galaxy-yml]
level: practitioner
status: docs-checked
description: "Scaffold a collection with ansible-galaxy collection init, then version it with semver rules, release branches, deprecation cycles and changelog fragments."
sources: ["Creating collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_creating.html)", "Distributing collections, versioning (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_distributing.html)", "Migrating content between collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_migrating.html)", "antsibull-changelog (https://github.com/ansible-community/antsibull-changelog/blob/main/docs/changelogs.md)", "ansible-core collection skeleton (https://github.com/ansible/ansible/tree/devel/lib/ansible/galaxy/data/default/collection)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scaffolding and versioning a collection

## Scaffold
```bash
ansible-galaxy collection init acme.platform --init-path ./collections/ansible_collections
tree acme/platform
# README.md  galaxy.yml  meta/runtime.yml  docs/  plugins/README.md  roles/   (the default skeleton)
```
Namespace and collection names use letters, digits and underscores, are at least three characters long and cannot start with an underscore. Create the skeleton in a path that includes `ansible_collections`.
Then add: `plugins/modules/`, `plugins/module_utils/`, `tests/sanity/`, `tests/unit/`, `tests/integration/targets/`, `changelogs/config.yaml` (`antsibull-changelog init .`), `.github/workflows/`. The `ansible-creator init collection acme.platform` tool generates a skeleton that includes an `extensions/molecule` directory.

Edit `galaxy.yml` (namespace, name, version, authors, license, dependencies, repository) and `meta/runtime.yml` (`requires_ansible: '>=2.15.0'`).

## Semantic versioning for collections
| Change | Bump |
|---|---|
| backwards compatible bug fix | patch (1.4.1 → 1.4.2) |
| new modules, plugins, parameters, return values (backwards compatible) | minor (1.4 → 1.5) |
| incompatible change | major (1.x → 2.0) |

For removals, the documented migration process deprecates the content with a `removal_version` scheduled for the next major version in `meta/runtime.yml` (`plugin_routing` → `deprecation`), then removes it in that major release and adds a `redirect`.

## Release flow
1. Every PR adds a changelog fragment: `changelogs/fragments/123-fix-timeout.yml` (`bugfixes:`, `minor_changes:`, `breaking_changes:`, `deprecated_features:`).
2. Release: bump `galaxy.yml` version, `antsibull-changelog release`, tag `1.5.0`, `ansible-galaxy collection build`, publish.

## Gotchas
- The version in galaxy.yml must change for every publish; Galaxy/hub reject duplicates.
- Pre-releases (`2.0.0-rc1`) are ignored by installs unless required explicitly with `==` or `--pre`.
- Keep `requires_ansible` accurate.

## Verify
```bash
ansible-galaxy collection build --force && ls acme-platform-*.tar.gz
```

## Checked

Checked 2026-10-26 against the Ansible collection documentation (creating, distributing, migrating), the antsibull-changelog docs and the ansible-core default collection skeleton. Confirmed: `collection init` and `--init-path` usage, skeleton contents, name rules, semantic versioning rules, changelog fragment sections (`bugfixes`, `minor_changes`, `breaking_changes`, `deprecated_features`), `antsibull-changelog init` and `release`, pre-release handling. Removed the unconfirmed community policy, stable-branch and ansible-creator tox and devcontainer claims.

Method: documentation only; no commands were run.
