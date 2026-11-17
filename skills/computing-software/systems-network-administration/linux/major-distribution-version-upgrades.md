---
id: computing-software.systems-network-administration.linux.major-distribution-version-upgrades
name: major-distribution-version-upgrades
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, distro-upgrade, release-upgrade, in-place-upgrade, leapp, do-release-upgrade, dnf-system-upgrade, debian-dist-upgrade, bookworm-upgrade, rhel-upgrade, ubuntu-lts-upgrade, elevate, rollback, lvm-snapshot-rollback, pre-upgrade-checklist, third-party-repos, lpic-2, maintenance, sysadmin, leapp-preupgrade, obsolete-packages]
level: advanced
status: gated
description: "Upgrade a Linux host in place: leapp (RHEL/Alma/Rocky), do-release-upgrade (Ubuntu), full-upgrade (Debian), dnf system-upgrade (Fedora), with checklist, rollback and cleanup."
sources:
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/upgrading_from_rhel_8_to_rhel_9/index
  - https://ubuntu.com/server/docs/how-to-upgrade-your-release
  - https://docs.fedoraproject.org/en-US/quick-docs/upgrading-fedora-offline/
licence: Apache-2.0
version: 6
updated: 2026-11-17
---

# Major distribution version upgrades — in place, with a way back

**Goal:** upgrade a host to the next major release without rebuilding it, and be
able to roll back in minutes if the application doesn't survive.

## 0. Decide: upgrade or rebuild?
Rebuild (new VM from image + config management + restore data) when the host is
cattle, config is in Ansible, or you're two releases behind. Upgrade in place when
the box is a pet with hand-grown state, downtime windows are short, and the vendor
supports the exact path (RHEL 8→9 yes; 7→9 no; Ubuntu LTS→LTS or sequential only;
Debian N→N+1 only; Fedora system-upgrade is supported over at most two releases).

## 1. Checklist before every upgrade
```bash
# backup & rollback point
borg create / restic backup …; lvcreate -s -L 20G -n root_pre /dev/vg0/root   # or VM snapshot / cloud image
sfdisk -d /dev/sda > /root/sda.sfdisk; vgcfgbackup; cp -a /etc /root/etc-pre-upgrade
# state
dnf repoquery --userinstalled > /root/pkgs.txt   # apt-mark showmanual > /root/pkgs.txt
rpm -qa --qf '%{NAME} %{VENDOR}\n' | grep -v 'Red Hat\|AlmaLinux\|Rocky\|Fedora' > /root/third-party.txt   # apt: apt list --installed | grep -v "$(lsb_release -cs)"
df -h /boot /var /   # ≥ 1 GiB /boot free (two kernels), several GiB in /var/cache
systemctl --failed; needs-restarting -r; uptime   # start from a clean, freshly rebooted, fully patched host
```
- Disable/remove third-party repos (EPEL, Docker, PostgreSQL, Node, Zabbix…) and their
  packages **or** know their new-release repos; they are the #1 cause of broken upgrades.
- Confirm applications support the new OS (Python/OpenSSL/glibc version jumps break
  things: RHEL 9 drops SHA-1 signatures, Debian 12 moves to merged-usr, Ubuntu 24.04
  removes `python2`).
- Run from the console/IPMI/serial, or inside `tmux`/`screen` over SSH with a second (gated: unconfirmed, source is paywalled or blocked)
  session open; network/sshd restarts mid-upgrade are normal.
- Window: 30–90 min plus app validation; announce it.

## 2. RHEL / AlmaLinux / Rocky: leapp
```bash
dnf update -y && reboot                                # must be on the latest minor of the source release
dnf install leapp-upgrade                              # RHEL: subscription + `leapp-upgrade-el8toel9`; Alma: `elevate-release` + leapp-data-almalinux
leapp preupgrade --target 9.4                          # Alma/Rocky: also pass the leapp-data package for the target
less /var/log/leapp/leapp-report.txt                   # "inhibitor" entries block; fix each (e.g. remove pata_acpi module, set PermitRootLogin, answer questions)
leapp answer --section remove_pam_pkcs11_module_check.confirm=True
leapp upgrade --target 9.4 && reboot                   # boots into an "upgrade" initramfs, installs, reboots again; 20-60 min
```
Post: `cat /etc/redhat-release`, `dnf repolist`, `rpm -qa | grep el8` (leftovers to remove), `leapp` leaves
`/var/log/leapp/`, re-enable third-party repos for el9, `dnf module reset` old streams,
`setenforce 1` if leapp set permissive, `systemctl list-units --failed`. Rocky/Alma use the
**ELevate** project (`elevate-release-latest-el8`), which also handles CentOS 7→8→9. Rollback =
snapshot restore; leapp has no undo.

## 3. Ubuntu: do-release-upgrade
```bash
apt update && apt full-upgrade -y && reboot
apt install ubuntu-release-upgrader-core
grep Prompt /etc/update-manager/release-upgrades     # lts = only LTS→LTS (22.04→24.04 opens with 24.04.1); normal = every release
do-release-upgrade                                    # -d for the not-yet-pointed release; it opens sshd on port 1022 as a fallback
```
It disables third-party sources (re-enable with the new codename after), removes obsolete
packages at the end (say yes, review the list), and keeps/overwrites conffiles interactively
(`N` keep yours by default; diff with `D`). Snaps upgrade themselves. Afterwards:
`apt autoremove --purge`, `lsb_release -a`, check `/etc/apt/sources.list.d/*.distUpgrade` leftovers,
`needrestart`. Rollback = snapshot.

## 4. Debian: edit sources, two-step upgrade
```bash
apt update && apt full-upgrade -y && reboot; apt autoremove --purge
dpkg --audit; apt-mark showhold                           # no half-configured or held packages
sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list /etc/apt/sources.list.d/*.list   # 12: non-free-firmware component is new; .sources files: edit Suites:
apt update
apt upgrade --without-new-pkgs -y                          # minimal step first (release-notes recommend it)
apt full-upgrade -y                                        # the real one; answer conffile prompts (keep yours, merge after)
reboot; apt autoremove --purge; apt purge '~o'             # obsolete packages
cat /etc/debian_version
```
`apt list '?obsolete'`, `dpkg -l | grep '^rc' | awk '{print $2}' | xargs apt purge -y` for config leftovers.
Read the release notes' "issues to be aware of" section — every release has 3–5 real ones
(e.g. 11→12: `/usr` merge, `systemd-resolved` split, `rsyslog` not default).

## 5. Fedora: dnf system-upgrade
```bash
dnf upgrade --refresh -y && reboot
dnf install dnf-plugin-system-upgrade                       # DNF4 only; DNF5 has system-upgrade built in
dnf system-upgrade download --releasever=<N>                # add --allowerasing only if it asks; review what it removes
dnf system-upgrade reboot                                     # offline upgrade in a minimal boot; then normal reboot
dnf distro-sync; rpmconf -a                                    # fix partial upgrades; merge .rpmnew files
```

## 6. After any upgrade
- Merge config: RHEL `rpmconf -a` or `find /etc -name '*.rpmnew' -o -name '*.rpmsave'`; Debian/Ubuntu
  `find /etc -name '*.dpkg-dist' -o -name '*.dpkg-old'`, `ucf --purge`.
- SELinux relabel if the policy changed majorly: `touch /.autorelabel && reboot` (RHEL 8→9 recommended).
- Regenerate initramfs and grub if the kernel line changed; verify `/boot/efi` entries (`efibootmgr -v`).
- Re-run config management (`ansible-playbook site.yml --check --diff`) — it shows the drift the upgrade introduced.
- Application smoke tests; then delete the LVM snapshot (`lvremove`) — a full snapshot gets
  dropped automatically and the rollback vanishes silently, so size it generously and watch `lvs`.

## Rollback
LVM: `lvconvert --merge /dev/vg0/root_pre` (merges on next reboot, reverting root) — only if
`/boot` is separate and unchanged or also snapshotted. VM/cloud: revert the snapshot/AMI.
No snapshot: reinstall and restore from backup — which is why §1 is not optional.

## Verify
- [ ] `cat /etc/os-release` shows the target; `uname -r` is the new kernel; `systemctl --failed` is empty.
- [ ] No packages from the old release remain (`rpm -qa | grep el8`, `apt list '?obsolete'`); third-party repos point at the new release.
- [ ] Application checks pass; the rollback snapshot was only removed after sign-off.

## Checked

2026-11-02

- Confirmed: The Fedora offline-upgrade page and the RHEL 8-to-9 upgrade guide index were fetched.
- Removed or gated: The Ubuntu upgrade page is a stub and the RHEL guide index lacks the leapp options; apt/dpkg/rpm flags and the upgrade procedure are gated, confirm in the current release notes and man pages.

Method: documentation only; no commands were run.
