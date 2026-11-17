---
id: computing-software.cryptography-implementation.key-management.operating-system-fips-mode
name: operating-system-fips-mode
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, fips-mode-setup, fips-140-3, rhel, ubuntu-pro, windows-fips-policy, crypto-policies, containers, fips-enabled]
level: practitioner
status: draft
description: "Enable and verify OS-level FIPS mode on RHEL, Ubuntu Pro and Windows, check that OpenSSL, Java and Go follow it, and understand container and vendor-claim caveats."
sources: ["https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/switching-rhel-to-fips-mode_security-hardening", "https://ubuntu.com/security/certifications/docs/fips-enablement", "https://learn.microsoft.com/en-us/windows/security/security-foundations/certification/fips-140-validation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Operating system FIPS mode

## RHEL
```
# RHEL 8/9
fips-mode-setup --enable && reboot
fips-mode-setup --check
cat /proc/sys/crypto/fips_enabled         # 1
update-crypto-policies --show            # FIPS
```
On RHEL 10 `fips-mode-setup` is gone: FIPS mode is chosen at installation (`fips=1` on the installer kernel command
line); converting a running system is not supported, so build images in FIPS mode from the start.

## Ubuntu (Pro subscription)
```
pro enable fips-updates      # or 'fips' for strictly certified packages without security updates
reboot
cat /proc/sys/crypto/fips_enabled
```
`fips-updates` ships security fixes on top of validated modules; `fips` stays at the exact certified versions.

## Windows
Group Policy: Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options >
"System cryptography: Use FIPS compliant algorithms for encryption, hashing, and signing" (registry
`HKLM\System\CurrentControlSet\Control\Lsa\FipsAlgorithmPolicy\Enabled = 1`). Microsoft only recommends it when
required by regulation; it blocks some non-approved algorithms in .NET and Schannel.

## Do applications follow it?
| Runtime | Behaviour |
|---|---|
| OpenSSL 3 on RHEL/Ubuntu FIPS | System config loads the FIPS provider; check `openssl list -providers` |
| Java (RHEL OpenJDK) | Switches to the FIPS-configured security providers when the system is in FIPS mode |
| Go | Use Go's native FIPS module (`GODEBUG=fips140=on` or `GOFIPS140` build setting) or distro Go with OpenSSL backend |
| Python | `hashlib.md5()` raises in FIPS mode unless `usedforsecurity=False` |

## Containers
The kernel flag is the host's; userspace crypto must be the validated packages inside the image (e.g. UBI images
in FIPS mode, Ubuntu Pro FIPS images). A FIPS host does not make an Alpine image FIPS.

## Gotchas
- "FIPS mode enabled" is not "FIPS validated": the module versions must match an active CMVP certificate.
- Some software hard-fails in FIPS mode (MD5 for non-security uses); test before enforcing.

## Verify
- [ ] `fips_enabled` is 1 and crypto policy shows FIPS.
- [ ] Application test: MD5 or non-approved cipher is refused in production paths.
