---
id: computing-software.systems-network-administration.linux.dnf-provides-groups-and-download
name: dnf-provides-groups-and-download
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dnf, yum, dnf-provides, whatprovides, dnf-download, dnf-groups, package-groups, environment-groups, repoquery, offline-install, rhel, fedora, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Find which package provides a file or command, install package groups and environments, and download RPMs with dependencies for offline hosts."
sources:
  - https://dnf.readthedocs.io/en/latest/command_ref.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/download.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_software_with_the_dnf_tool/index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnf provides, groups and download

**Goal:** get from "I need `semanage`" or "I need a dev toolchain" to the right packages,
including on hosts without internet.

## 1. Which package provides it
```bash
dnf provides semanage                 # which package provides the command
dnf provides '*/bin/dig'              # glob on path
dnf provides 'libssl.so.3()(64bit)'   # library soname
dnf repoquery --whatrequires openssl-libs --installed   # who depends on it
dnf repoquery -l nginx                # files in a package (--list)
rpm -qf /usr/sbin/sshd                # owner of an installed file
dnf search --all tcpdump              # name+summary+description
```

## 2. Groups and environments
```bash
dnf group list --hidden               # environments + groups (ids in parentheses)
dnf group info "Development Tools"    # mandatory / default / optional packages
dnf group install "Development Tools" # mandatory+default
dnf group install --with-optional "Virtualization Host"
dnf group install "Server with GUI"   # an environment group (dnf4: environment ids too)
dnf group remove "Development Tools"
dnf group mark install "System Tools" # dnf4: mark the group installed
```
Kickstart/`dnf install @development @^server-product-environment`: `@` prefix = group,
`@^` = environment. Group membership comes from repo `comps.xml`.

## 3. Download for offline install
```bash
dnf download nginx                                   # just the rpm into cwd
dnf download --resolve --alldeps nginx --destdir=/tmp/pkgs   # all deps, not skipping already-installed ones
dnf download --resolve nginx --destdir=/tmp/pkgs     # --resolve also downloads dependencies
dnf download --source nginx                          # SRPM
dnf install --downloadonly --downloaddir=/tmp/pkgs nginx     # same resolver as a real install
# on the offline host:
dnf install /tmp/pkgs/*.rpm
```

## Gotchas
- `--alldeps` (with `--resolve`) does not skip dependencies already installed on this host; without it the set is relative to this host.
- `dnf group remove` removes the group's packages that do not belong to another installed group and were not installed explicitly; check with `--assumeno` first.
- dnf5 has an `optional_metadata_types` option (values include `filelists`) controlling which optional metadata is downloaded; see `man dnf5.conf`.

## Verify
- [ ] `rpm -qf $(command -v <cmd>)` matches what `dnf provides` said.
- [ ] `dnf group list --installed` shows the group after install (`--installed` narrows the list).

## Checked

Checked against dnf4 command_ref.rst (rpm-software-management/dnf, last push 2026-10-23), dnf-plugins-core download.rst (last push 2026-10-22) and the dnf5 provides, download and group docs.
Confirmed: `group info/install --with-optional/list --hidden/remove/mark install`, `@group` spec, `--downloadonly` with `--downloaddir`, plugin `download` with `--resolve`, `--alldeps`, `--source` and `--destdir`, repoquery `--whatrequires`/`--list`/`--installed`, dnf5 `provides` and `optional_metadata_types`.
Removed as unconfirmed: the example package name for semanage, the `@^` environment syntax, same-minor-version advice, createrepo_c and reposync remarks, the claim that dnf4 tracks group state in a separate database.

Method: documentation only; no commands were run.
