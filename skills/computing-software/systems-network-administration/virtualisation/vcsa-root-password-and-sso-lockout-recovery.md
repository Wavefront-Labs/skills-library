---
id: computing-software.systems-network-administration.virtualisation.vcsa-root-password-and-sso-lockout-recovery
name: vcsa-root-password-and-sso-lockout-recovery
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcsa-root-password, sso-admin-lockout, vcsa, vcenter-sso, password-expiry, vmware, vsphere]
level: advanced
status: docs-checked
description: "Recover an expired or forgotten VCSA root password via GRUB, unlock administrator@vsphere.local with vdcadmintool, and set expiry so it does not recur."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2147144
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VCSA root password and SSO admin lockout

The VCSA root password **expires after 90 days by default**. Expiry locks you out of
VAMI and SSH and breaks patching. The vCenter Single Sign-On domain administrator is not
affected by the SSO lockout policy, but its password can still be lost or forgotten.

## Root expired but known
SSH or console login forces a change. Or in VAMI → Administration → Password expiration
settings, set expiry (or "No") and an email warning. CLI:
```sh
chage -l root
chage -M 365 -W 14 root        # or -M -1 to disable expiry, if policy allows
```

## Root forgotten (needs console + reboot, take a snapshot first)
1. Snapshot the VCSA (offline-safe point), reboot from the VM console.
2. At GRUB press `e` (8.x GRUB password may be set at deploy, ask the deployer).
3. On the `linux` line append `rw init=/bin/bash`, boot with F10.
4. `mount -o remount,rw /` then `passwd root`; if the account was locked by PAM:
   `/usr/sbin/faillock --user root --reset` (from 8.0 U2, pam_tally2 is deprecated in
   Photon 4; older releases use `pam_tally2 -u root -r`).
5. `umount /` and reboot (`reboot -f`). Delete the snapshot after validation.

## administrator@vsphere.local locked or forgotten
SSH as root, then:
```sh
shell
/usr/lib/vmware-vmdir/bin/vdcadmintool
#  3 = Reset account password (enter administrator@vsphere.local) -> prints a generated password
#  0 = exit
```
Log in with the generated password and change it. To unlock without reset, wait the
unlock interval or have another SSO admin unlock via Administration → Single Sign On →
Users and Groups.

## Prevent
- Set root expiry to match policy and **monitor** it (alarm or script: `chage -l`).
- Keep a second break-glass SSO admin in the vsphere.local domain, password in the vault.
- SSO lockout policy defaults: 5 consecutive failed attempts within 3 minutes, automatic
  unlock after 5 minutes; service accounts with stale passwords cause repeat lockouts, so
  find the source in the SSO logs on the VCSA.

## Verify
`chage -l root` shows the new expiry; VAMI login works; SSO admin login works and
vCenter services are running (check with `service-control`).

## Checked
2026-10-31: The 90-day root password expiry, VAMI password expiration settings, `chage -M 99999`, the GRUB recovery approach and the pam_tally2 deprecation (faillock from 8.0 U2) confirmed in KB 2147144; the SSO lockout defaults (5 attempts / 3 minutes / 5-minute unlock) and the administrator exemption confirmed on the vCenter Password Requirements and Lockout Behavior page. Removed unconfirmed specifics: the SSO log file names and the exact `service-control --status --all` invocation.
Method: documentation only; no commands were run.
