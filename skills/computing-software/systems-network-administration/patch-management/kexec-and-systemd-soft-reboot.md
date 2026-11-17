---
id: computing-software.systems-network-administration.patch-management.kexec-and-systemd-soft-reboot
name: kexec-and-systemd-soft-reboot
category: computing-software
field: systems-network-administration
product: patch-management
tags: [kexec, soft-reboot, systemd-soft-reboot, kernel-update, patch-reboots, linux]
level: practitioner
status: docs-checked
description: "Shorten Linux patch reboots with kexec (skip firmware POST) and systemd soft-reboot (userspace only), knowing when each actually applies kernel and library fixes."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-soft-reboot.service.html
  - https://man7.org/linux/man-pages/man8/kexec.8.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
  - https://github.com/systemd/systemd/blob/main/NEWS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kexec and systemd soft-reboot

Physical servers can spend a long time in firmware initialisation. These tools skip parts of the reboot.

## kexec: new kernel without firmware
Loads the new kernel into memory and jumps to it; firmware, RAID controller init and PXE are skipped. Applies kernel updates.
```sh
# load the new kernel first (version numbers are placeholders)
kexec -l /boot/vmlinuz-<new-version> --initrd=/boot/<initrd-for-new-version> --reuse-cmdline
systemctl kexec        # clean shutdown of services, then jump
```
`systemctl kexec` loads a kexec kernel only if one was not loaded yet, otherwise it fails unless `--force` is given (which performs a normal reboot). Once a kernel is loaded with `kexec --load`, a plain `reboot` also uses kexec unless `SYSTEMCTL_SKIP_AUTO_KEXEC=1` is set.

Caveats: on systems with locked-down Secure Boot the kernel must be loaded with the `KEXEC_FILE_LOAD` syscall (`kexec -s`) so its signature is verified, and `KEXEC_LOAD` may be disabled in the kernel configuration. Firmware-level updates (BIOS, device firmware) are not applied.

## systemd soft-reboot (systemd 256 and later)
Restarts all of userspace (stops every unit, re-executes the service manager, optionally switching into a new root mounted at `/run/nextroot/`) while keeping the **same running kernel**. Kernel settings such as sysctl values are not reset.
```sh
systemctl soft-reboot
```
Applies updates to userspace (libraries and services) without the hardware reboot, firmware, boot loader, kernel and initrd phases. Does **not** apply kernel or firmware/microcode updates.

## Decide per update
| Pending | Use |
|---|---|
| Kernel update | kexec (or full reboot for firmware/microcode) |
| glibc/systemd/openssl only | soft-reboot, or restart services via needrestart |
| Firmware/BIOS/microcode | full reboot |

## Gotchas
- Monitoring may not see a kexec as a reboot (uptime resets, but no BMC power event); patch compliance checks should compare `uname -r` to the installed kernel, not uptime.
- Test kexec per hardware model once; failures leave a hung host needing out-of-band console.
- Live-patching (kpatch/Livepatch/ksplice) is a separate option that avoids reboots for selected CVEs.

## Verify
After kexec: `uname -r` equals newest installed kernel. After soft-reboot: `needs-restarting -s` (EL) or `needrestart -b` shows no services using deleted libraries.

## Checked

Checked 2026-10-27 against the systemd documentation (systemd 262 manual pages and NEWS), the kexec manual page and kexec-tools source.
- `systemctl soft-reboot` and `systemctl kexec` behaviour, `SYSTEMCTL_SKIP_AUTO_KEXEC`, `/run/nextroot/`, kernel not reset in a soft-reboot: confirmed. The old "systemd 254+" gate was wrong: NEWS lists the soft-reboot mechanism under systemd 256.
- `kexec -l ... --initrd= --reuse-cmdline`, and `-s` (KEXEC_FILE_LOAD, needed for signature verification under locked-down Secure Boot): confirmed.
- Corrected: `systemctl kexec` does not pick the default boot entry; it needs a kernel loaded beforehand or fails.
- Removed unconfirmed: POST duration, the Debian `LOAD_KEXEC` default-file setting and microcode/driver caveats.
Method: documentation only; no commands were run.
