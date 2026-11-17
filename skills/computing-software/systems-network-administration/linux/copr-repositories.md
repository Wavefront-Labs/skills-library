---
id: computing-software.systems-network-administration.linux.copr-repositories
name: copr-repositories
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dnf, copr, dnf-copr, third-party-repos, fedora, epel, rhel, package-repositories, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Use Fedora COPR repositories safely: enable/disable with dnf copr, judge trustworthiness, pin chroots for RHEL/EPEL, and publish your own builds with copr-cli."
sources:
  - https://dnf-plugins-core.readthedocs.io/en/latest/copr.html
  - https://copr.fedorainfracloud.org/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# COPR repositories

**Goal:** get a package that isn't in Fedora/EPEL from a COPR project — knowing it's
community-built — or publish your own RPMs for a fleet without running a repo server.

## 1. Enable / disable
```bash
dnf install dnf-plugins-core                      # provides "dnf copr"
dnf copr enable owner/project                     # enable the repository
dnf copr enable owner/project <chroot>            # optional explicit chroot
dnf copr list --enabled                           # also --installed (default) and --disabled
dnf copr disable owner/project
dnf copr remove owner/project
dnf install thepackage
```
The default hub is https://copr.fedorainfracloud.org; `--hub` or `hub/owner/project` selects another.

## 2. Is it trustworthy?
COPR projects are built from whatever their owners upload, so review them yourself. Check on the project page:
owner, source, build history and update frequency, and which chroots are kept current. To stop a COPR repo
from replacing core packages, restrict it in the generated repo file with `includepkgs=` (or `excludepkgs=`):
```ini
includepkgs=thepackage*
```

## 3. Publish your own
```bash
dnf install copr-cli
# API token from https://copr.fedorainfracloud.org/api/ → ~/.config/copr
copr-cli create myproject --chroot fedora-rawhide-x86_64    # --chroot may be given several times
copr-cli build myproject mypkg-1.0-1.src.rpm
copr-cli buildscm myproject --clone-url https://git.example.com/mypkg.git --spec mypkg.spec
```
Webhooks can trigger builds on push (see the Copr user documentation).

## Gotchas
- A COPR repo with a higher version of a distro package can replace it; the `includepkgs` filter prevents surprise replacements.

## Verify
- [ ] `dnf repolist` shows the COPR repo.
- [ ] `dnf upgrade --assumeno` doesn't propose replacing core packages from COPR.

## Checked

Checked against dnf-plugins-core copr.rst (last push 2026-10-22), the Copr user documentation (fedora-copr/copr, last push 2026-10-23) and the copr-cli man page source.
Confirmed: `dnf copr enable/disable/remove/list/search`, optional chroot, `list --installed|--enabled|--disabled`, default hub and `--hub`, `includepkgs`/`excludepkgs`, `copr-cli create --chroot` (repeatable), `copr-cli build`, `copr-cli buildscm --clone-url --spec`, token in `~/.config/copr` from the Copr API page, webhooks exist.
Fixed: dropped the non-existent `copr-cli list-builds`. Removed as unconfirmed: generated repo file name, signing-key and gpgcheck claims, repo-listing filter, Fedora upgrade and Satellite remarks.

Method: documentation only; no commands were run.
