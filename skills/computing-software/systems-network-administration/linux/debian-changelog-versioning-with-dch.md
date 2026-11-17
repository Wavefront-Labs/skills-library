---
id: computing-software.systems-network-administration.linux.debian-changelog-versioning-with-dch
name: debian-changelog-versioning-with-dch
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dch, debian-changelog, debian-packaging, version-numbering, devscripts, local-rebuild]
level: practitioner
status: docs-checked
description: "Maintain debian/changelog with dch: new versions, local rebuild suffixes (+local1, ~bpo), distribution fields, UNRELEASED, and how version ordering decides upgrades."
sources:
  - https://manpages.debian.org/bookworm/devscripts/dch.1.en.html
  - https://www.debian.org/doc/debian-policy/ch-source.html#debian-changelog-debian-changelog
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# debian/changelog with dch

`debian/changelog` sets the package version; dpkg reads the top entry.
```
mytool (1.4.2-1) bookworm; urgency=medium

  * New upstream release.
  * Fix config path handling (Closes: #1012345)

 -- Ops Team <ops@example.com>  Sat, 18 Oct 2026 10:00:00 +0000
```
Format is strict: the trailer line starts with exactly one space and the maintainer and date are separated by exactly two spaces (deb-changelog(5)); let `dch` write it.

## dch
```bash
export DEBEMAIL=ops@example.com DEBFULLNAME="Ops Team"
dch -v 1.4.3-1 "New upstream release."          # new version
dch -i "Rebuild with patch for CVE-2026-1234"     # increment debian revision
dch --local corp "Internal rebuild"               # adds a local suffix to the Debian version
dch --bpo                                          # increments the release for a backports upload and adds a backport changelog comment
dch -a "Another change"                            # append to current entry
dch -r                                             # release: UNRELEASED becomes the previous entry's distribution
```

## Version ordering (dpkg --compare-versions)
`[epoch:]upstream[-revision]`. `~` sorts **before** anything (1.0~rc1 < 1.0), `+` after (1.0 < 1.0+corp1).
```bash
dpkg --compare-versions 1.4.2-1+corp1 gt 1.4.2-1 && echo newer      # + sorts after the end of a part
```
A `+` suffix sorts after the base version and a `~` suffix before it (deb-version(5)); pick the one that matches whether a local rebuild should win over the same Debian version.

## Gotchas

## Verify
- [ ] `dpkg-parsechangelog -S Version` prints the intended version; `dpkg-buildpackage -us -uc` produces `.deb`s with that version.

## Checked

Checked against dch(1) on manpages.debian.org (bookworm), deb-changelog(5) and deb-version(5) (guillemj/dpkg, 2026-10).
Confirmed: dch `-v`, `-i`, `-a`, `-r`, `--local`, `--bpo`, `--create`, `--package`, DEBEMAIL/DEBFULLNAME; trailer-line spacing rules; tilde sorts before everything.
Fixed: the exact result strings of `--local` and `--bpo` are not documented, so the examples no longer show them. Removed as unconfirmed: epoch advice, lintian and tarball-name remarks.

Method: documentation only; no commands were run.
