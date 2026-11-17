---
id: computing-software.systems-network-administration.linux.kernel-module-signature-enforcement
name: kernel-module-signature-enforcement
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kernel-modules, module-sig-enforce, module-signing, sign-file, secure-boot, lockdown, required-key-not-available]
level: advanced
status: docs-checked
description: "Handle kernel module signing: module.sig_enforce, Secure Boot lockdown, 'Key was rejected by service' errors, signing a module with sign-file and enrolling the key via MOK."
sources:
  - https://www.kernel.org/doc/html/latest/admin-guide/module-signing.html
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_monitoring_and_updating_the_kernel/signing-a-kernel-and-modules-for-secure-boot_managing-monitoring-and-updating-the-kernel
  - https://wiki.debian.org/SecureBoot
  - https://docs.kernel.org/admin-guide/module-signing.html
  - https://github.com/lcp/mokutil/blob/master/man/mokutil.1
  - https://github.com/dell/dkms/blob/master/dkms.8.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel module signature enforcement

**Symptom:** `modprobe` fails to insert a module — the kernel refuses a module that is unsigned or signed with an unknown key when enforcement is on.

## Why it happens
- Kernel built with `CONFIG_MODULE_SIG`; enforcement is on when `module.sig_enforce=1` is on the kernel command line or `CONFIG_MODULE_SIG_FORCE=y`. Secure Boot policy can also require signatures; check your distribution's documentation.
- Check Secure Boot state: `mokutil --sb-state`.
- Without enforcement, unsigned modules load but taint the kernel and the module is marked with the `E` taint character.

## Inspect a module
```bash
keyctl list %:.builtin_trusted_keys     # keys built into the kernel (the kernel documents this keyring)
```

## Sign your own module (out-of-tree / DKMS)
```bash
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der \
  -nodes -days 36500 -subj "/CN=<org> module signing/"
mokutil --import MOK.der            # prompts for a one-time password; complete enrolment at the next boot
scripts/sign-file sha256 MOK.priv MOK.der $(modinfo -n mymod)   # sign-file ships in the kernel tree or your distribution's kernel-devel/headers package
```
DKMS can sign automatically: set `mok_signing_key` and `mok_certificate` in `/etc/dkms/framework.conf`.

## Gotchas
- Never disable Secure Boot as the "fix" on managed fleets — sign instead.
- Keep the private key off the build host or protected; anyone with it can load kernel code.
- MOK enrolment is completed at the next boot — plan console access for remote boxes.

## Verify
- [ ] `mokutil --test-key MOK.der` reports the key state; `modprobe mymod` loads; `cat /proc/sys/kernel/tainted` is unchanged.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (admin-guide/module-signing, kernel-parameters), the mokutil man page source and the DKMS man page source on 2026-10-26. Confirmed: `CONFIG_MODULE_SIG`, `CONFIG_MODULE_SIG_FORCE`, `module.sig_enforce=1`, unsigned modules load but taint with `E` when not enforced, `.builtin_trusted_keys` keyring, `scripts/sign-file <hash> <priv> <x509> <module>` argument order, `mokutil --sb-state`, `--import`, `--password`, `--test-key`, DKMS `mok_signing_key` and `mok_certificate`. Removed: exact modprobe error strings, lockdown file, `.platform` keyring, distro sign-file paths, compressed-module and Ubuntu key-path claims.

Method: documentation only; no commands were run.
