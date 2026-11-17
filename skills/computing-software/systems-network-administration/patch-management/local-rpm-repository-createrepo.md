---
id: computing-software.systems-network-administration.patch-management.local-rpm-repository-createrepo
name: local-rpm-repository-createrepo
category: computing-software
field: systems-network-administration
product: patch-management
tags: [createrepo, patch-repository, reposync, linux-patching, dnf, updateinfo]
level: practitioner
status: docs-checked
description: "Build and serve local RPM repositories with createrepo_c: layout, keeping updateinfo for security filtering, GPG signing, incremental updates and client .repo configuration."
sources:
  - https://github.com/rpm-software-management/createrepo_c
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/reposync.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local RPM repositories with createrepo_c

Use for internal packages, vendor RPMs not in a repo, or a curated mirror for air-gapped
sites.

## Create
```sh
dnf install createrepo_c httpd
mkdir -p /srv/repos/internal/el9/x86_64
cp *.rpm /srv/repos/internal/el9/x86_64/
createrepo_c /srv/repos/internal/el9/x86_64
createrepo_c --update /srv/repos/internal/el9/x86_64      # incremental after adding RPMs
```
Serve with httpd/nginx (`/srv/repos` as document root) or a file share.

## Keep security metadata when mirroring
`dnf --security` and `dnf updateinfo` need `updateinfo.xml`. reposync can download it:
```sh
dnf reposync --repoid=<repo-id> --download-metadata --newest-only -p /srv/repos/mirror
```
`--download-metadata` downloads all upstream repository metadata and the copy is usable as a repository without running createrepo_c; with `--newest-only` the metadata still lists older packages. If you regenerate with
createrepo_c, re-add it:
```sh
modifyrepo_c --mdtype=updateinfo updateinfo.xml /srv/repos/mirror/baseos/repodata
```
`--mdtype` sets the metadata type (derived from the file name when omitted). Modular repositories also carry modules metadata that must be preserved.

## Sign
Sign packages with rpm's signing tooling and/or the repository metadata (`repo_gpgcheck` verifies a signature on the metadata), and publish the public key. See the rpm and createrepo_c documentation for the exact signing commands for your release.

## Client
```ini
# /etc/yum.repos.d/internal.repo
[internal]
name=Internal EL9
baseurl=http://repo.corp.example/internal/el9/$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=http://repo.corp.example/keys/RPM-GPG-KEY-internal
```
`dnf clean metadata && dnf repolist && dnf list --repo internal`.

## Gotchas
- `gpgcheck=0` to "make it work" defeats integrity: sign instead.
- Large repos: `--update` reuses existing metadata for unchanged RPMs (by size and mtime) and `--workers` sets how many workers read RPMs.
- Mirrors of vendor content such as RHEL need a valid entitlement for reposync; check your subscription terms before exposing them to anyone outside your organisation.

## Verify
`dnf updateinfo list --security` on a client against the mirror returns advisories;
`dnf install <pkg>` succeeds with gpgcheck and repo_gpgcheck on.

## Checked

Checked 2026-10-27 against the createrepo_c and modifyrepo_c manual pages (upstream repository) and the DNF reposync plugin and configuration pages.
- `dnf reposync --repoid ... --download-metadata --newest-only -p <path>`: confirmed.
- `createrepo_c --update` and `--workers`: confirmed. `modifyrepo_c --mdtype`: confirmed.
- `gpgcheck`, `repo_gpgcheck` repo options (both default False): confirmed.
- Removed unconfirmed: the example RHEL repo id, the package and metadata signing command lines, the explicit modules mdtype value.
Method: documentation only; no commands were run.
