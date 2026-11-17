---
id: computing-software.cloud-infrastructure-engineering.talos-linux.secureboot-boot-and-install
name: secureboot-boot-and-install
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [secureboot, uki, systemd-boot, image-factory, tpm, securitystate, enrollment, installer-secureboot]
level: advanced
status: docs-checked
description: "Boot and install Talos in SecureBoot mode with Sidero Labs signed images: setup mode, key enrollment, the secureboot installer, TPM encryption patch, securitystate, upgrades."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/platform-specific-installations/bare-metal-platforms/secureboot.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos boots UEFI systems in SecureBoot mode using `systemd-boot` and a signed Unified Kernel Image (UKI) holding kernel, initramfs and cmdline. SecureBoot is not supported for x86 BIOS mode, and a GRUB-based install cannot be upgraded to UKI, so a fresh install is needed. SecureBoot images exist from Talos v1.5.0.

Start from the Image Factory SecureBoot ISO (`https://factory.talos.dev/image/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba/<version>/metal-amd64-secureboot.iso`) on a UEFI machine with SecureBoot enabled and in setup mode. Keys enroll automatically only in virtual machines (default `secure-boot-enroll` is `if-safe`); on bare metal press Esc and pick `Enroll Secure Boot keys: auto`, or build an image with `secure-boot-enroll` set to `force`.

Verify in maintenance mode:

```shell
talosctl -n <IP> get securitystate --insecure
```

Generate config with the SecureBoot installer and a TPM encryption patch (`tpm: {}` keys in slot 0 on `STATE` and `EPHEMERAL` `VolumeConfig` documents):

```sh
talosctl gen config <cluster-name> https://<endpoint>:6443 --install-image=factory.talos.dev/metal-installer-secureboot/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba:<version> --install-disk=/dev/sda --config-patch @tpm-disk-encryption.yaml
talosctl -n <IP> apply-config --insecure -f controlplane.yaml
```

Detach the ISO after install, then check `talosctl -n <IP> --talosconfig=talosconfig get securitystate`.

With SecureBoot on, the UKI ignores command line arguments passed at boot and uses those embedded in it, so changing kernel args, adding an extension or bumping the version means rebuilding the UKI and installer, then upgrading with the new installer. Keep the UKI signing key and PCR signing key or the node cannot boot the new UKI and unlock encrypted partitions.

## Checked

2026-11-04. ISO path, enrollment modes, securitystate check, gen config command, kernel args behaviour and key preservation warning confirmed on the SecureBoot page.

Method: documentation only; no commands were run.
