---
id: computing-software.systems-network-administration.linux.secure-boot-and-tpm
name: secure-boot-and-tpm
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, secure-boot, uefi, tpm, tpm2, measured-boot, mokutil, mok, shim, dkms-signing, kernel-module-signing, sbctl, efivars, pcr, tpm2-tools, systemd-cryptenroll, uki, unified-kernel-image, systemd-stub, lockdown, lpic-2, security, boot, sysadmin]
level: advanced
status: docs-checked
description: "Operate Linux under UEFI Secure Boot and TPM 2.0: check state, enrol MOK keys so DKMS modules load, sign kernels/UKIs with your own keys, bind LUKS to PCRs, and recover when boot is refused."
sources:
  - https://wiki.debian.org/SecureBoot
  - https://manpages.debian.org/unstable/mokutil/mokutil.1.en.html
  - https://github.com/Foxboron/sbctl/blob/master/docs/sbctl.8.txt
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-cryptenroll.html
  - https://www.freedesktop.org/software/systemd/man/latest/ukify.html
  - https://man7.org/linux/man-pages/man7/kernel_lockdown.7.html
  - https://github.com/dkms-project/dkms/blob/main/dkms.8.in
  - https://github.com/tpm2-software/tpm2-tools/tree/master/man
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Secure Boot and TPM — boot only signed code, and prove it

**Goal:** keep Secure Boot enabled (not "disable it to make the driver load"), get
third-party modules signed and trusted, optionally own the signing chain, and use the TPM
to unlock disks only when the boot path is unmodified.

## 1. Where am I
```bash
mokutil --sb-state                 # SecureBoot enabled/disabled
bootctl status                     # firmware, Secure Boot, TPM2 support, current entry
dmesg | grep -iE 'secure boot|lockdown'   # lockdown messages (see kernel_lockdown(7))
ls /sys/firmware/efi/efivars | head; efibootmgr -v
ls /dev/tpmrm0                             # TPM2 resource-manager device node (also used by systemd-cryptenroll)
tpm2_getcap properties-fixed               # fixed TPM properties
```
The usual chain (Debian wiki): most x86 firmware trusts binaries signed by Microsoft; the distro's `shim` loader is signed by Microsoft and embeds the distro's key, which then vouches for the bootloader and kernel. Out-of-tree modules built locally (DKMS) are not signed by the distro key, so with Secure Boot enforcement they are refused until you sign them with a key you have enrolled.

## 2. Enrol a MOK and sign out-of-tree modules
```bash
# Debian's DKMS generates a key and you enrol it with: mokutil --import /var/lib/dkms/mok.pub (Debian wiki)
# Ubuntu keeps its auto-generated MOK in /var/lib/shim-signed/mok/ (Debian wiki)
# Generic key (the Debian wiki uses RSA 2048; it reports shim problems with 4096-bit keys):
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der -nodes -days 36500 -subj "/CN=Example MOK/"
mokutil --import MOK.der                       # prompts for a one-time password
reboot                                         # follow UEFI's on-screen instructions to confirm the enrollment with that password
mokutil --list-enrolled | grep -i example
# sign a module (repeat for every kernel/module rebuild; DKMS can be configured to do it)
/lib/modules/$(uname -r)/build/scripts/sign-file sha512 MOK.priv MOK.der /lib/modules/$(uname -r)/extra/foo.ko   # usage: sign-file <hash> <key> <cert> <module>
modinfo foo | grep -E 'sig_key|signer'
```
- DKMS: set `mok_signing_key` and `mok_certificate` in `/etc/dkms/framework.conf` (the dkms man page; the Debian wiki shows `/var/lib/shim-signed/mok/MOK.priv` and `MOK.der`) so rebuilds auto-sign. If either file is missing, dkms re-creates both files.
- Lost the MOK password / wrong key: `mokutil --reset` (see mokutil(1) for its confirmation steps), reboot, re-import.
- The MOK is as powerful as the distro key for module loading — keep `MOK.priv` `0600 root` or off-box.

## 3. Owning the chain (appliances, labs, UKI setups)
```bash
sbctl status
sbctl create-keys                              # creates the Platform Key, Key Exchange Key and Signature Database key
sbctl enroll-keys --microsoft                  # also enrol Microsoft's vendor certificates (see "Option ROM" in sbctl(8)); the firmware must be in Setup Mode
sbctl sign -s /boot/efi/EFI/Linux/*.efi        # sign and remember files for re-signing on update
sbctl verify
```
`ukify` combines kernel, initrd and command line into one Unified Kernel Image and can sign it, so the signature covers the initramfs and the command line too. Enrolling only your own keys can stop option ROMs (for example GPU firmware) that are signed with Microsoft keys from running; sbctl's `--microsoft` flag exists for that case (sbctl(8), "Option ROM").

## 4. TPM 2.0: measured boot and sealed secrets
```bash
tpm2_pcrread sha256:0,1,4,7,11                # 0 platform code (firmware), 1 platform config, 4 boot loader code, 7 Secure Boot policy, 11 kernel-boot (systemd-stub)
systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 /dev/nvme0n1p3            # LUKS auto-unlock when SB state unchanged
systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=0+7 --tpm2-with-pin=yes …   # + firmware + PIN
systemd-cryptenroll --recovery-key /dev/nvme0n1p3                              # ALWAYS, before relying on TPM
# crypttab: luks-… UUID=… none tpm2-device=auto,discard
# regenerate the initramfs (dracut -f or update-initramfs -u) with TPM2 unlocking support included
```
- PCR choice is a trade-off: `7` alone survives firmware updates but not disabling Secure
  Boot; `0+7` catches firmware changes and therefore needs the recovery key after every
  BIOS update. `11` with a UKI binds to the exact kernel — pair with `systemd-pcrlock` or
  signed PCR policies (`--tpm2-public-key`) to survive kernel updates.
- Measured boot is only as useful as what checks it, such as the LUKS policy above or remote attestation. Reading PCRs after the fact tells you something changed, not what.
- `tpm2_clear` (or clearing the TPM in firmware) loses the objects created under the cleared hierarchies, including sealed secrets — enroll a recovery key first (see tpm2_clear(1)).

## 5. When boot is refused
- A firmware or shim signature-verification error on boot means an unsigned or untrusted kernel or
  bootloader. Boot a signed distro kernel from the firmware menu, or temporarily disable SB
  in firmware **to fix the signing**, not as the end state.
- Module silently absent after kernel update: DKMS rebuilt but didn't sign — check `modinfo <module>` for signature fields and the kernel log (`journalctl -k`) for module signature or key errors.
- Changing Secure Boot keys or settings changes what other software measured or protected with them (for example other operating systems' disk encryption); check their documentation before touching SB settings on a dual-boot machine.
- VMs: use a virtual TPM and Secure Boot-capable firmware in your hypervisor to test any of this safely.

## Verify
- [ ] `mokutil --sb-state` = enabled; `dmesg | grep -i lockdown` shows the lockdown message; the out-of-tree module loads (`lsmod`).
- [ ] `sbctl verify` (or `mokutil --list-enrolled`) shows every boot-path file signed.
- [ ] LUKS unlocks via TPM on a normal boot; after toggling Secure Boot off it falls back to the recovery key — then re-enable and re-enrol.

## Checked
Checked 2026-10-27 against the Debian SecureBoot wiki, mokutil(1), the sbctl README and sbctl(8) source, systemd man page sources (systemd-cryptenroll, crypttab, bootctl, ukify), kernel_lockdown(7), the dkms man page source and the tpm2-tools manual sources.
- Debian wiki: shim is signed by Microsoft and embeds the distro key; `mokutil --import` prompts for a one-time password and enrolment is confirmed at reboot; `mokutil --sb-state`; Ubuntu's MOK lives in /var/lib/shim-signed/mok/; the wiki generates the key with the same `openssl req` command (RSA 2048) and sets `mok_signing_key`/`mok_certificate` in /etc/dkms/framework.conf; `sign-file` from the kernel build directory; `modinfo` shows module signatures.
- mokutil: `--import`, `--list-enrolled`, `--reset`, `--sb-state`. sbctl: `create-keys`, `enroll-keys --microsoft` (with an Option ROM warning), `sign -s`, `verify`, Setup Mode. dkms man page: `mok_signing_key`, `mok_certificate` (files re-created if missing).
- systemd-cryptenroll: `--tpm2-device=auto`, `--tpm2-pcrs=` (plus-separated list), `--tpm2-with-pin`, `--recovery-key`, `--tpm2-public-key`, systemd-pcrlock; PCR meanings 0 platform-code, 1 platform-config, 4 boot-loader-code, 7 secure-boot-policy, 11 kernel-boot; crypttab `tpm2-device=`; `ukify` builds and signs Unified Kernel Images.
- tpm2-tools: `tpm2_pcrread`, `tpm2_getcap properties-fixed`, `tpm2_clear` (objects under cleared hierarchies are lost).
- Removed unconfirmed claims: Ubuntu `update-secureboot-policy`, RHEL/Fedora akmods and kmodgenca, Clevis, Keylime, BitLocker, firmware error strings, lockdown mode names, distro-specific sign-file paths, `/var/lib/sbctl` permissions and dracut module names.
Method: documentation only; no commands were run.
