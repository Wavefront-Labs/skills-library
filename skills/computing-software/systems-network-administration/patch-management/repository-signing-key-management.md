---
id: computing-software.systems-network-administration.patch-management.repository-signing-key-management
name: repository-signing-key-management
category: computing-software
field: systems-network-administration
product: patch-management
tags: [repo-signing-key, apt-key-deprecation, patch-integrity, signature-verification, signed-by, gpg]
level: practitioner
status: docs-checked
description: "Manage package repository signing keys safely: APT signed-by keyrings instead of apt-key, RPM key import and rotation, handling expired vendor keys, and auditing trusted keys."
sources:
  - https://manpages.debian.org/stable/apt/sources.list.5.en.html
  - https://manpages.ubuntu.com/manpages/noble/man8/apt-key.8.html
  - https://rpm-software-management.github.io/rpm/man/rpmkeys.8
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/deb822_repository_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repository signing key management

## APT: per-repository keyrings (apt-key is deprecated)
`apt-key add` put keys into a global trust store: any key could sign any repo. Use
`signed-by` so each key is trusted only for its repo.
```sh
install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://packages.vendor.example/key.gpg | gpg --dearmor -o /etc/apt/keyrings/vendor.gpg
chmod 0644 /etc/apt/keyrings/vendor.gpg
```
deb822 source (`/etc/apt/sources.list.d/vendor.sources`):
```
Types: deb
URIs: https://packages.vendor.example/apt
Suites: stable
Components: main
Signed-By: /etc/apt/keyrings/vendor.gpg
```
Verify the key fingerprint against the vendor's published value before trusting:
`gpg --show-keys /etc/apt/keyrings/vendor.gpg`.
Migrate legacy keys: list with `apt-key list` (or files in `/etc/apt/trusted.gpg.d/`), move each
to `/etc/apt/keyrings/` and add `Signed-By`.

## RPM
```sh
rpmkeys --import https://packages.vendor.example/RPM-GPG-KEY-vendor    # rpm --import is the same operation
rpmkeys --list                                                        # trusted keys
rpmkeys --delete <fingerprint>                                        # remove an old key
rpmkeys --checksig package.rpm                                        # verify signature (rpm -K)
```
`.repo` files: `gpgcheck=1`, `repo_gpgcheck=1` where metadata is signed, `gpgkey=` URL or file.

## Expired or rotated vendor keys
Symptom: `apt-get update` or `dnf makecache` reports a missing, expired or invalid repository signing key. Fix: fetch the vendor's **new** key from an authenticated source
(vendor docs over HTTPS), verify fingerprint, replace the keyring file. Never set
`[trusted=yes]` or `gpgcheck=0` as a fix.

## Fleet management
Distribute keyrings and source files via config management (Ansible `get_url` +
`deb822_repository` / `yum_repository` modules) with pinned fingerprints; audit trusted keys
across hosts quarterly and alert on unknown ones.

## Verify
`apt-get update` / `dnf makecache` without signature warnings; audit shows each third-party
repo has its own signed-by keyring and no legacy apt-key entries remain.

## Checked
Date: 2026-10-27. Documentation checked: sources.list(5) (`Signed-By`, recommended keyring locations `/usr/share/keyrings` for packages and `/etc/apt/keyrings` for the operator, `trusted` option, deb822 format), apt-key(8) (deprecated), `ansible.builtin.deb822_repository` (`signed_by`), rpm(8) and rpmkeys(8) (`--import`, `--checksig`, `--list`, `--delete`), dnf.conf reference (`gpgcheck`, `repo_gpgcheck`, `gpgkey`), GnuPG manual (`--show-keys`, `--dearmor`). Replaced the `rpm -q gpg-pubkey` and `rpm -e gpg-pubkey` commands with rpmkeys, and the unconfirmed error strings with a neutral description. The previous Debian wiki source blocks automated access and is replaced by manual pages.

Method: documentation only; no commands were run.
