---
id: computing-software.cloud-infrastructure-engineering.ansible.downloading-collections-for-offline-transfer
name: downloading-collections-for-offline-transfer
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-galaxy, collection-download, offline-install, air-gapped-collections]
level: practitioner
status: docs-checked
description: "Use ansible-galaxy collection download to fetch collections and dependencies as tarballs with a generated requirements file, then install them offline."
sources: ["Downloading collections (https://docs.ansible.com/ansible/latest/collections_guide/collections_downloading.html)", "Verifying collections (https://docs.ansible.com/ansible/latest/collections_guide/collections_verifying.html)", "ansible-galaxy CLI source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/galaxy.py)", "podman-save (https://docs.podman.io/en/latest/markdown/podman-save.1.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Downloading collections for offline transfer

## On a connected host
```bash
ansible-galaxy collection download -r requirements.yml -p ./offline-collections
ls offline-collections/     # <namespace>-<name>-<version>.tar.gz files plus requirements.yml
```
- Dependencies are downloaded too; the default download folder is `./collections` (`-p` / `--download-path` changes it).
- A `requirements.yml` for installing the downloaded collections is generated in the output directory.
- Collections given as a URL or tarball path are downloaded again from the configured Galaxy server.
- Use `--no-deps` only if you will resolve dependencies yourself.

## Transfer and install on the air-gapped host
```bash
cd offline-collections
ansible-galaxy collection install -r requirements.yml -p /srv/proj/collections
```
or individually: `ansible-galaxy collection install ./<namespace>-<name>-<version>.tar.gz`. Run the requirements install from the folder that contains the downloaded files.

## Python and system dependencies
Collections do not install their Python dependencies; collect each collection's `requirements.txt` and mirror the packages with pip's own offline workflow (see the pip documentation).
For execution environments, build the EE on the connected side and transfer the image (`podman save -o ee.tar <image>` and `podman load -i ee.tar`) instead.

## Verify integrity
```bash
sha256sum *.tar.gz > SHA256SUMS            # record before transfer, check after
ansible-galaxy collection verify <namespace>.<name> --offline   # checks installed content against locally stored data (signed collections installed from a distribution server)
```

## Gotchas
- `collection verify` does not support tarball requirements; use `namespace.name` entries (or `--ignore-errors`).
- Pin exact versions before downloading so the offline set matches what was tested.

## Verify
- [ ] `ansible-galaxy collection list` on the offline host shows every expected version.

## Checked

Checked 2026-10-26 against the Ansible collections guide (downloading and verifying pages), ansible-core devel `cli/galaxy.py` (`download` options `-p/--download-path`, `-n/--no-deps`, `--pre`) and the podman-save documentation (output to a file with `-o`). Confirmed the download behaviour, generated `requirements.yml`, install-from-that-folder note, and `verify --offline` semantics and tarball limitation. Removed unconfirmed pip wheel command specifics, the 2.12 version gate, the hub import claim and example package names.

Method: documentation only; no commands were run.
