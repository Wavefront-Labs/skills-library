---
id: computing-software.cloud-infrastructure-engineering.ansible.listing-and-verifying-installed-collections
name: listing-and-verifying-installed-collections
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-galaxy, collections-usage, collection-verify, galaxy-list, collection-list, ansible-galaxy-collection-list, collections-path]
level: practitioner
status: docs-checked
description: "See which collection versions Ansible will actually load with ansible-galaxy collection list, detect shadowed duplicates, and verify installed files against the Galaxy server."
sources: ["Listing collections (https://docs.ansible.com/ansible/latest/collections_guide/collections_listing.html)", "Verifying collections (https://docs.ansible.com/ansible/latest/collections_guide/collections_verifying.html)", "ansible-galaxy CLI source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/galaxy.py)", "ansible-navigator configuration source (https://github.com/ansible/ansible-navigator/blob/main/src/ansible_navigator/configuration_subsystem/navigator_configuration.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing and verifying installed collections

## Which versions are installed, and which wins
```bash
ansible-galaxy collection list                       # every collection in every collections_path
ansible-galaxy collection list community.general     # one collection, all locations
ansible-galaxy collection list -p ./collections      # extra search path, added to the front of the configured paths
ansible-galaxy collection list --format json         # also human (default) or yaml
ansible-config dump | grep COLLECTIONS_PATHS
```
Output is grouped by path:
```
# <PROJECT_DIR>/collections/ansible_collections
Collection        Version
----------------- -------
community.general 9.5.0

# /usr/share/ansible/collections/ansible_collections
Collection        Version
----------------- -------
community.general 8.6.0
```
`collections_path` is an ordered list of search paths, so check which copy comes first. Collections under development with a `galaxy.yml` instead of `MANIFEST.json` are shown with `*` as the version. `-vvv` shows more detail. The list can include collections that were installed only as dependencies of others.

## Reading docs of what is installed
`ansible-doc community.general.ufw` (the FQCN is required to show a plugin's documentation); inside an EE, `ansible-navigator collections` (explore available collections) or `ansible-navigator doc community.general.ufw`.

## Verify integrity
```bash
ansible-galaxy collection verify community.general           # compares the installed content with the collection on the server
ansible-galaxy collection verify -r requirements.yml
ansible-galaxy collection verify community.general --offline --keyring ~/.ansible/pubring.kbx   # signed collections: uses data saved at install time
ansible-galaxy collection verify acme.internal --keyring ~/.ansible/pubring.kbx   # plus signatures
```
The command is quiet on success; if a collection was modified the altered files are listed under its name. Use `-vvv` for the versions, paths and the remote URL used.

## Gotchas
- If you do not give a version, `verify` checks against the latest version on the server; name the version for pre-release or older installs. Dependencies in requirements.yml are not verified; tarball and URL entries are not supported (use `--ignore-errors`).
- Collections inside the pip `ansible` package should not be managed directly with `ansible-galaxy`; install newer ones into a configured collections path, which takes precedence over collections found in `PYTHONPATH`.
- `ANSIBLE_COLLECTIONS_PATH` overrides the config file; CI and laptops can differ silently, so print it in CI logs.

## Verify
- [ ] Exactly one copy of each required collection appears, or the intended copy is first.
- [ ] `collection verify -r requirements.yml` passes in CI.

## Checked

Checked 2026-10-26 against the Ansible collections guide (listing and verifying pages), ansible-core `cli/galaxy.py` (`list --format {human,yaml,json}`, `-p` behaviour, PYTHONPATH precedence warning) and ansible-navigator `collections` subcommand. Confirmed the list output format, `verify` behaviours (quiet success, version default, `--offline`, `--keyring`, requirements limits). Removed the unconfirmed `jq` pipeline, `ansible-doc -F`, shadowing and "added or missing files" claims.

Method: documentation only; no commands were run.
