---
id: computing-software.cloud-infrastructure-engineering.ansible.installing-local-rpm-and-deb-files
name: installing-local-rpm-and-deb-files
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, packages-repos, local-rpm, deb-file, vendor-packages, gpg-check]
level: practitioner
status: docs-checked
description: "Install vendor .rpm and .deb files from a URL or a copied file with dnf and apt, keep it idempotent, verify signatures, and prefer an internal repo for fleets."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/dnf_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/apt_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/rpm_key_module.html", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/dnf.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/apt.py", "https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/rpm_key.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing local rpm and deb files

## RPM
```yaml
- name: Import vendor signing key
  ansible.builtin.rpm_key:
    key: https://vendor.example.com/RPM-GPG-KEY-vendor
    fingerprint: "ABCD 1234 ..."       # pin it

- name: Install agent from URL
  ansible.builtin.dnf:
    name: https://vendor.example.com/agent-3.2.1-1.el9.x86_64.rpm
    state: present

- name: Or from a file shipped with the role
  ansible.builtin.copy: {src: agent-3.2.1-1.el9.x86_64.rpm, dest: /var/tmp/}
- ansible.builtin.dnf:
    name: /var/tmp/agent-3.2.1-1.el9.x86_64.rpm
    state: present
    disable_gpg_check: false
```
The dnf module's `name` accepts a package specifier, a URL or a local path to an rpm file.
`rpm_key` accepts a URL, a file on the managed node or a key id, and `fingerprint` (a list) verifies the key being imported.

## DEB
```yaml
- name: Install from URL
  ansible.builtin.apt:
    deb: https://vendor.example.com/agent_3.2.1_amd64.deb

- name: From a local file (on the target)
  ansible.builtin.apt:
    deb: /var/tmp/agent_3.2.1_amd64.deb
```
`deb` is the path to a .deb package on the remote machine; if the path contains `://` the module downloads it first.
It requires the `xz-utils` package on the target to read the package control file.

## Upgrades
Both `dnf` and `apt` have `allow_downgrade` (apt since 2.12), which lets the named package and version replace an already
installed higher version; the docs warn it can make the module non-idempotent. Put the version in a variable and the file name in one place.

## Prefer a repository for fleets
For more than a handful of hosts, publish packages in an internal repository and use `yum_repository`
or `deb822_repository` plus `dnf`/`apt` by name, so normal repository updates apply.

## Gotchas
- `disable_gpg_check: true` affects packages installed from a repository as well as local and URL packages (module docs). Prefer importing the key with `rpm_key`.
- To fetch a large file from an internal mirror, `get_url` with `checksum: sha256:<digest>` verifies the download.

## Verify
- [ ] A second run reports no change, and the package manager on the host lists the expected version.

## Checked
Checked 2026-10-26 against ansible-core devel `dnf.py`, `apt.py` and `rpm_key.py` documentation blocks (repository
last commit 2026-10-23). Confirmed: dnf `name` takes URL or rpm path, `disable_gpg_check` scope, `allow_downgrade` in dnf and apt
(2.12), apt `deb` URL download and `xz-utils` requirement, `rpm_key` `key`/`fingerprint`. Removed unconfirmed claims: NEVRA
comparison, repeated URL downloads, apt-versus-dpkg dependency handling, version-skip behaviour, repository product names,
file-name quoting and the `rpm -K` check.
Method: documentation only; no commands were run.
