---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-and-ansible-core-version-matrix
name: ansible-and-ansible-core-version-matrix
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, control-node, core-version-matrix, support-lifecycle, porting-guide]
level: practitioner
status: docs-checked
description: "Map the ansible community package to its ansible-core version, read the support lifecycle, and choose versions supporting your control and target Pythons."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html", "https://docs.ansible.com/ansible/latest/porting_guides/porting_guides.html", "https://docs.ansible.com/ansible/latest/roadmap/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ansible vs ansible-core version matrix

Two things are versioned separately:
- **ansible-core**: the engine, CLI tools and `ansible.builtin`. A new major release roughly every 6 months, in May and November (2.15, 2.16, 2.17, 2.18 ...).
- **ansible** (community package): ansible-core plus more than 85 collections. Each community major version pairs with one core minor (ansible 9 → core 2.16, 10 → 2.17, 11 → 2.18, 12 → 2.19, 13 → 2.20, 14 → 2.21).

```bash
pip show ansible ansible-core | grep -E 'Name|Version'
ansible --version                 # shows the core version only
ansible-community --version       # community package version (shown in the installation guide)
```

## Support lifecycle
Each core release gets general bug and security fixes at GA, then critical and security fixes, then security fixes only, then EOL; maintenance covers three releases. The release-and-maintenance page has a table of control-node and target Python ranges per core version: check it before upgrading because core regularly drops old Pythons (core 2.17 requires target Python 3.7 or newer, so Python 2.7 and 3.6 targets need core 2.16 or earlier; core 2.17 control nodes need Python 3.10 to 3.12). From core 2.16 targets support the 6 most recent Python versions (7 every sixth release), and control nodes the 3 most recent.

## Choosing
| Situation | Pick |
|---|---|
| Minimal EE, collections pinned in requirements.yml | ansible-core only |
| Laptop/quick start | ansible community package |
| RHEL 8 targets with platform-python 3.6 | core <= 2.16 or install a newer Python on targets |

## Upgrading safely
1. Read the porting guide for each core minor you jump (2.15 → 2.16 → 2.17).
2. Run `ansible-lint` and the full Molecule suite on the new version in a separate venv.
3. Watch deprecation warnings in the current version first — they become errors next release.

## Gotchas
- `pip install ansible==10.*` drags its matching core; `pip install -U ansible-core` alone can leave the community package's collections expecting a different core.
- Collections declare `requires_ansible` in meta/runtime.yml; a too-old core prints a warning and modules may fail.

## Verify
- [ ] Control and target Pythons are inside the supported range for the chosen core.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in reference_appendices/release_and_maintenance.rst: community package pairings 8 to 14 and core versions, more than 85 collections, May/November cadence, three maintained core releases, Python ranges (2.17 control 3.10-3.12, target 3.7-3.12; 2.16 targets include Python 2.7 and 3.6), target rule from 2.16.
- Confirmed `ansible-community --version` appears in the installation guide.
- Release state at check time: community package 14 is current (core 2.21); package 15 and core 2.22 are in development per the stable-2.22 docs.
- Removed unconfirmed claims: AAP lifecycle paragraph and EE image name.

Method: documentation only; no commands were run.
