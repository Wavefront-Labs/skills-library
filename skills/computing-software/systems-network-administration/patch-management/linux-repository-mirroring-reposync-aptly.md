---
id: computing-software.systems-network-administration.patch-management.linux-repository-mirroring-reposync-aptly
name: linux-repository-mirroring-reposync-aptly
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-acquisition, patch-repository, reposync, aptly, repository-snapshot, local-mirror, dnf, apt, patch-management, linux-patching]
level: practitioner
status: docs-checked
description: "Mirror Linux repositories for controlled patching: dnf reposync + createrepo, aptly mirrors and dated snapshots, publishing, and pointing clients at the snapshot for each ring."
sources:
  - https://www.aptly.info/doc/overview/
  - https://dnf-plugins-core.readthedocs.io/en/latest/reposync.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mirroring Linux repositories (reposync, aptly)

**Goal:** every server in a ring installs exactly the same package set, tested in the
pilot ring, without each one hitting the internet.

## RHEL family: reposync
```sh
dnf install -y dnf-plugins-core createrepo_c
dnf reposync --repoid=baseos --repoid=appstream --download-metadata --newest-only \
    -p /srv/mirror/el9/$(date +%F)
```
`--download-metadata` downloads all repository metadata, including updateinfo (errata), so `dnf updateinfo list --security` can work on clients. With `--newest-only` the metadata still lists older packages whose RPM files were not downloaded and DNF then errors; run `createrepo_c --update` on the mirror directory to drop them.
Serve with nginx/httpd; point clients with a `.repo` file
(`baseurl=http://mirror.<domain>/el9/2026-10-14/baseos/`).

## Debian/Ubuntu: aptly
```sh
aptly mirror create -architectures=amd64 noble-sec http://security.ubuntu.com/ubuntu noble-security main universe
aptly mirror update noble-sec
aptly snapshot create noble-sec-2026-10-14 from mirror noble-sec
aptly publish snapshot -distribution=noble-security noble-sec-2026-10-14 ubuntu-sec
# next cycle, switch the published distribution to a new snapshot:
aptly publish switch noble-security ubuntu-sec noble-sec-2026-11-11
```
Sign published repos with your GPG key and distribute the public key to clients.

## Dated snapshots per ring
- Snapshot the mirror on Patch Tuesday +1 (or your cadence).
- Pilot ring points at the new snapshot; broad rings keep the previous one until the pilot
  passes, then move. Rollback = point back at the older snapshot (for future installs;
  already-installed packages need downgrade).
- Larger estates can use a dedicated content-management product for the same snapshot-per-ring idea.

## Gotchas
- Mirror only the repos and architectures you use; full mirrors are hundreds of GB.
- Mirrors without GPG verification of upstream defeat package signing; keep `gpgcheck=1`
  on clients and verify upstream signatures on sync (reposync `--gpgcheck` removes downloaded packages that fail the check, but not for repositories with `gpgcheck=0`).
- Monitor sync jobs: a silently failing mirror means nobody gets patches.

## Verify
`dnf repolist -v` / `apt-cache policy` on a client shows the mirror URL and snapshot date;
`dnf updateinfo list --security` returns advisories; the mirror's last sync is recent.

## Checked
Date: 2026-10-27. Documentation checked: dnf-plugins-core reposync page (`--repoid`, `-p/--download-path`, `-n/--newest-only`, `--download-metadata`, `--gpgcheck`, the `createrepo_c --update` note), DNF command reference (`--security`, `updateinfo`, `repolist -v`), aptly pages for `mirror create` (architectures) and `publish switch` (usage, in-place switch of a published snapshot). Added the newest-only metadata caveat and the reposync GPG caveat; removed the unconfirmed RHEL-subscription comment and product list.

Method: documentation only; no commands were run.
