---
id: computing-software.firmware-embedded-development.bootloader-development.u-boot-verified-boot
name: u-boot-verified-boot
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [u-boot, u-boot-verified-boot, fit-signature, mkimage-k, required-key, signed-configurations, rsa-2048, control-dtb, firmware-embedded-development]
level: sme
status: docs-checked
description: "Enable U-Boot verified boot: sign FIT configurations with mkimage, embed the public key in U-Boot's control DTB as required, and close the bypass holes."
sources:
  - https://docs.u-boot.org/en/latest/usage/fit/verified-boot.html
  - https://docs.u-boot.org/en/latest/usage/fit/signature.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# U-Boot verified boot

**Goal:** U-Boot refuses to boot a kernel/DTB/initramfs that isn't signed by your key,
extending the SoC's secure-boot chain (ROM verifies SPL/U-Boot) up to Linux.

## Signing
Add signature nodes to **configurations** (sign configurations, not just images: signing
images alone allows a mix-and-match attack, where the FIT's configuration is changed to select
different signed images, and a roll-back attack, substituting a signed image from an older FIT):
```dts
configurations {
    default = "conf-1";
    conf-1 {
        kernel = "kernel-1"; fdt = "fdt-1"; ramdisk = "ramdisk-1";
        signature-1 {
            algo = "sha256,rsa2048";
            key-name-hint = "prod";
        };
    };
};
```
```
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out keys/prod.key
openssl req -batch -new -x509 -key keys/prod.key -out keys/prod.crt
mkimage -f fit.its -k keys -K u-boot.dtb -r fitImage
```
`-K u-boot.dtb` writes the public key into U-Boot's control device tree; `-r` marks the key
**required** (`required = "conf"` or `"image"` in the key node), and only required keys are
normally verified by the FIT boot algorithm. Every image referenced by the configuration needs at
least one hash subnode. Rebuild U-Boot with that DTB so the key is inside the image the ROM
verifies.

## U-Boot config
```
CONFIG_FIT_SIGNATURE=y
CONFIG_RSA=y                      # CONFIG_ECDSA for ECDSA signing
```
Leave `CONFIG_LEGACY_IMAGE_FORMAT` undefined: with required signature checks it is off by default,
and enabling it lets old uImages bypass verification.

## Closing bypasses
- Disable legacy image formats and raw `booti`/`bootz` commands, or restrict the command set
  (`CONFIG_CMD_*`), since they boot unsigned kernels.
- Lock the console (or remove it) and the environment (writable list), otherwise
  `bootargs`/`bootcmd` can be changed.
- Root filesystem must also be verified (dm-verity with the root hash in the signed
  initramfs or kernel cmdline) or the attacker just modifies userspace.
- Keep the private key in an HSM/offline signing service; use `-N pkcs11` with mkimage.
- Plan key rotation: U-Boot supports multiple keys and signatures; `required-mode` in the
  `/signature` node is `any` or `all`.

## Verify
- [ ] `bootm` of the signed FIT verifies the signature (see the vboot sandbox tests on the signature page for sample output).
- [ ] Flipping one byte in the kernel inside the FIT: boot refused.
- [ ] An unsigned FIT and a legacy uImage are both refused.

## Checked
2026-10-31. Confirmed against the U-Boot FIT signature and verified boot pages: sha256,rsa2048 algo, key-name-hint, signed configurations vs mix-and-match and roll-back attacks, mkimage `-K ... -r`, required = conf/image, required-mode any/all, multiple keys, `-N pkcs11`, CONFIG_FIT_SIGNATURE, CONFIG_RSA, CONFIG_ECDSA, legacy image format default-off. Removed `sign-images` (the page says it is not used), `CONFIG_FIT_SIGNATURE_MAX_SIZE`, `EXT_DTB`, `CONFIG_BOOTM_NETBSD`, `CONFIG_AUTOBOOT_KEYED` and the literal bootm output line.
Method: documentation only; no commands were run.
