---
id: computing-software.systems-network-administration.linux.distribution-conversion-convert2rhel-migrate2rocky
name: distribution-conversion-convert2rhel-migrate2rocky
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, convert2rhel, migrate2rocky, almalinux-deploy, centos-migration, el-conversion, leapp]
level: practitioner
status: draft
description: "Convert CentOS and other EL clones in place with convert2rhel, migrate2rocky or almalinux-deploy: prerequisites, pre-conversion analysis, rollback and post-conversion checks."
sources:
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/converting_from_a_linux_distribution_to_rhel_using_the_convert2rhel_utility/index
  - https://docs.rockylinux.org/guides/migrate2rocky/
  - https://wiki.almalinux.org/documentation/migration-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Distribution conversion (convert2rhel/migrate2rocky)

In-place conversion swaps the vendor's packages, signing keys, repos and branding without reinstalling. It **doesn't** change major version: convert CentOS 7 to RHEL 7 then Leapp to 8, or CentOS Stream 8/9 only to matching minor states supported by the tool.

## Before any tool
- Full backup or VM snapshot. Rollback inside the tools is partial at best.
- Latest packages of the source distro (`yum update`), reboot into the newest kernel.
- Remove third-party kernel modules (old ZFS/DKMS), unsupported kernels, and conflicting repos.
- Check free space in `/var` and `/boot`, working DNS and access to target repos (or a local Satellite/mirror).

## convert2rhel (to RHEL)
```bash
curl -o /etc/yum.repos.d/convert2rhel.repo https://ftp.redhat.com/redhat/convert2rhel/<el-version>/convert2rhel.repo
yum install convert2rhel
convert2rhel analyze --org <org-id> --activationkey <key> -y     # pre-conversion report, no changes
less /var/log/convert2rhel/convert2rhel-pre-conversion.txt
convert2rhel --org <org-id> --activationkey <key> -y
reboot
```
Supported sources: CentOS Linux 7/8, Oracle Linux 7/8, AlmaLinux and Rocky 8/9 (check the current support matrix). Red Hat Insights can run the analysis fleet-wide.

## migrate2rocky / almalinux-deploy
```bash
curl -O https://raw.githubusercontent.com/rocky-linux/rocky-tools/main/migrate2rocky/migrate2rocky.sh
bash migrate2rocky.sh -r        # -r runs the migration; logs to /var/log/migrate2rocky.log
curl -O https://raw.githubusercontent.com/AlmaLinux/almalinux-deploy/master/almalinux-deploy.sh
bash almalinux-deploy.sh        # from CentOS 8, Rocky 8/9, Oracle Linux, RHEL
```
Both script `dnf distro-sync` against the new vendor's repos after swapping release packages.

## After conversion
```bash
cat /etc/os-release; rpm -qa --qf '%{VENDOR}\n' | sort | uniq -c   # leftover old-vendor packages
rpm -qa | grep -iE 'centos|oracle' | grep -v release
grubby --default-kernel; uname -r    # booted into the new vendor kernel?
dnf check; dnf repolist; subscription-manager status   # RHEL
```
- Re-sign/re-enrol Secure Boot shim if conversion changed it (convert2rhel handles shim; check `mokutil --sb-state`).
- Update monitoring, CMDB, and config management facts (`ansible_distribution`) so playbooks pick the right branches.

## Verify
- [ ] `os-release` and kernel show the target distro; no packages from the old vendor except where intended.
- [ ] Application smoke tests pass after reboot; subscription/entitlement active.
