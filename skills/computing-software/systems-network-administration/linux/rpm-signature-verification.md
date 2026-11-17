---
id: computing-software.systems-network-administration.linux.rpm-signature-verification
name: rpm-signature-verification
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rpm, dnf, rpm-checksig, gpgcheck, repo-gpgcheck, rpm-import, package-signing, rpm-verify, supply-chain, rhel, fedora, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Verify RPMs are genuine and intact: import and audit trusted keys, rpm -K/checksig on files, gpgcheck and repo_gpgcheck in repos, and rpm -V to detect tampered installed files."
sources:
  - https://github.com/rpm-software-management/rpm/blob/master/docs/man/rpmkeys.8.scd
  - https://github.com/rpm-software-management/rpm/blob/master/docs/man/rpm.8.scd
  - https://rpm-software-management.github.io/rpm/manual/signatures_digests.html
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RPM signature verification

**Goal:** only install packages signed by keys you trust, and check installed files haven't
been modified since.

## 1. Trusted keys
```bash
rpmkeys --list                                    # fingerprint, name and user id of each key
rpm --import <keyfile>                            # same as rpmkeys --import
rpmkeys --export <fingerprint>                    # export a key
rpmkeys --erase <fingerprint>                     # remove a key you no longer trust
```
Import third-party keys only after checking the fingerprint against the vendor's published value, not from the same mirror as the packages.

## 2. Check a package file
```bash
rpmkeys -K package.rpm      # --checksig (rpm -K is the same)
# package.rpm: digests signatures OK
rpmkeys -K --verbose package.rpm    # per-verifiable detail for troubleshooting
```
Output is per class: classes that verify are lowercase, failing classes UPPERCASE, and the final
conclusion under the verification policy is `OK` or `NOT OK`.

## 3. Enforce in dnf
```ini
# /etc/yum.repos.d/vendor.repo
[vendor]
baseurl=https://repo.vendor.example/el9/
gpgcheck=1                    # package signatures
repo_gpgcheck=1               # signed repomd.xml (metadata), if the repo supports it
gpgkey=https://repo.vendor.example/RPM-GPG-KEY-vendor
```
`localpkg_gpgcheck=1` in dnf.conf also checks local package files (documented default False). dnf's `gpgcheck`
can only strengthen the active RPM security policy (`%_pkgverify_level`). Do not set `gpgcheck=0` to "make it work".

## 4. Verify installed files
```bash
rpm -V openssh-server              # nothing printed = matches package metadata
rpm -Va 2>/dev/null | grep -v '^.......T'    # whole system, ignore mtime-only changes
```
Result codes: `S` size, `M` mode, `5` digest, `D` device, `L` symlink path, `U` user, `G` group, `T` mtime, `P` capabilities;
`.` = passed, `?` = could not be tested. A trailing attribute letter such as `c` marks a %config file.
A size and digest change on a binary needs investigation; changes to `c` files are often your own edits.

## Gotchas

## Verify
- [ ] Every enabled repo has `gpgcheck=1` (`grep -L 'gpgcheck=1' /etc/yum.repos.d/*.repo` empty).
- [ ] `rpmkeys -K` on a downloaded package reports `digests signatures OK`.
- [ ] `rpm -Va` output reviewed; only expected config-file changes remain.

## Checked

Checked against rpmkeys(8) and rpm(8) (rpm-software-management/rpm docs/man, last push 2026-10-22) and dnf4 conf_ref.rst (gpgcheck, repo_gpgcheck, localpkg_gpgcheck).
Confirmed: `rpmkeys --checksig/--list/--import/--export/--erase`, checksig output format, `--verify` result codes and attribute letters, `gpgcheck`, `repo_gpgcheck`, `localpkg_gpgcheck` and their defaults.
Removed as unconfirmed: the `gpg-pubkey` package query, key directory listing, version gate for `rpmkeys --list`, NOKEY wording, SHA-1 policy remark, key bundle and expiry remarks, the whole-system verify pipeline and forensic remark. Replaced the vendor-site sources with the rpm documentation.

Method: documentation only; no commands were run.
