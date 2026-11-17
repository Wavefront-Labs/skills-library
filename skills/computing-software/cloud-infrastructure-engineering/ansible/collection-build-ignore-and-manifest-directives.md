---
id: computing-software.cloud-infrastructure-engineering.ansible.collection-build-ignore-and-manifest-directives
name: collection-build-ignore-and-manifest-directives
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collection-development, build-ignore, manifest-directives, galaxy-yml, collection-build, distlib, tarball-contents]
level: advanced
status: docs-checked
description: "Control exactly which files go into a collection tarball with galaxy.yml build_ignore or the manifest directives (MANIFEST.in style), and check the result before publishing."
sources: ["Distributing collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_distributing.html)", "Collection structure (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)", "MANIFEST.in commands (https://packaging.python.org/en/latest/guides/using-manifest-in/)", "Collection verification (https://docs.ansible.com/ansible/latest/collections_guide/collections_verifying.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collection build_ignore and manifest directives

Goal: the built `namespace-name-x.y.z.tar.gz` contains the collection and nothing else — no
`.venv`, CI secrets, test output, or 200 MB of fixtures.

By default `ansible-galaxy collection build` packs **everything** in the directory except a
small built-in list (`.git/`, `*.pyc`, `*.retry`, `tests/output`, previous tarballs in the root, `galaxy.yml`
itself). Other VCS directories are excluded too.

## Option A: build_ignore (glob exclusions)
```yaml
# galaxy.yml
build_ignore:
  - .github
  - .venv
  - "*.tar.gz"
  - tests/output
  - tests/integration/targets/*/files/large-*
  - docs/build
  - .env
```
Patterns are glob-like: `*`, `?`, `[seq]` and `[!seq]` are supported. `build_ignore` needs ansible-core 2.10 or newer.

## Option B: manifest directives (ansible-core 2.14+, needs `pip install distlib`)
```yaml
# galaxy.yml  (cannot be combined with build_ignore)
manifest:
  directives:
    - recursive-exclude tests/integration/targets/*/files *.iso
    - exclude .env
    - prune docs/build
    - recursive-include docs/docsite *.rst *.yml
  omit_default_directives: false
```
With `omit_default_directives: false` your lines are inserted after the default includes and before the default excludes. The defaults include `meta/*.yml`, top-level text files such as README and LICENSE, `tests`, `docs`, `roles`, `playbooks`, `changelogs` and `plugins` content, and exclude `galaxy.yml`, `MANIFEST.json`, `FILES.json`, previous tarballs, `tests/output` and dotfiles and `__pycache__`. Setting it `true` means you must list *everything* to include (see the documentation for a starting set). The directives use the Python packaging MANIFEST.in command syntax (for example `include`, `exclude`, `recursive-include`, `recursive-exclude`, `global-exclude`, `prune`). To use the defaults without adding directives write `manifest: {}`.

Use manifest when you need include-lists (allow-list packaging), build_ignore for a few excludes.

## Check what got packed
```bash
ansible-galaxy collection build --force
tar -tzf acme-platform-2.1.0.tar.gz | sort | less
tar -tzf acme-platform-2.1.0.tar.gz | grep -E '\.venv|\.env|tests/output|secret' && echo "LEAK"
ls -lh acme-platform-2.1.0.tar.gz
```
`MANIFEST.json` and `FILES.json` inside the tarball carry the collection metadata and file list. `ansible-galaxy collection verify` compares an installed collection's checksums with the remote collection (or, with `--offline`, with local data).

## Gotchas
- `build_ignore` and `manifest` together: build fails — choose one.
- Manifest mode requires the optional `distlib` Python package; add it to the build requirements.
- The current Galaxy maximum tarball size is 20 MB; large fixtures belong outside the tarball.

## Verify
- [ ] `tar -tzf` listing contains only intended paths and the leak grep returns nothing.
- [ ] `ansible-galaxy collection install ./acme-platform-2.1.0.tar.gz -p /tmp/c` and a smoke playbook works.

## Checked

Checked 2026-10-26 against the Ansible documentation (ansible-documentation devel, `developing_collections_distributing.rst`, `collections_verifying.rst`). Confirmed: default tarball exclusions, `build_ignore` wildcard characters and ansible-core 2.10 gate, manifest directives needing `distlib`, ansible-core 2.14 gate and mutual exclusivity with `build_ignore`, `manifest: {}`, default directive order and `omit_default_directives`, the 20 MB Galaxy tarball limit, `verify` behaviour. Removed the unconfirmed `.gitignore`, error text and `ansible-test` certification claims.

Method: documentation only; no commands were run.
