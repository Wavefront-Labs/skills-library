---
id: computing-software.cloud-infrastructure-engineering.talos-linux.imager-custom-boot-assets
name: imager-custom-boot-assets
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [imager, boot-assets, iso, installer, extra-kernel-arg, system-extension-image]
level: sme
status: docs-checked
description: "Build custom Talos assets offline with imager: profiles, flags like --extra-kernel-arg and --system-extension-image, crane lookups, registry auth, ISO, installer."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/platform-specific-installations/boot-assets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Image Factory covers official releases and extensions. For `main` branch builds, local changes or custom extensions use the `imager` container (`ghcr.io/siderolabs/imager:<version>`; its signature can be verified).

```sh
docker run --rm -t \
  -v "$PWD/_out:/secureboot:ro" \
  -v "$PWD/_out:/out" \
  ghcr.io/siderolabs/imager:<version> \
  <image-kind> [optional: customization]
```

`<image-kind>` profiles: `iso`, `secureboot-iso`, `metal`, `secureboot-metal`, `secureboot-installer`, plus platform names like `aws`, `gcp`, `azure`. Customization flags: `--arch`, `--meta <key>=<value>`, `--extra-kernel-arg` (prefix with `-` to remove a default such as `-console` or `-console=tty0`), `--system-extension-image`, and `--image-cache`.

Imager needs full image references, found with crane:

```sh
crane export ghcr.io/siderolabs/extensions:<version> | \
  tar x -O image-digests | \
  grep EXTENSION-NAME
```

Overlays are looked up the same way from `ghcr.io/siderolabs/overlays:<version>` (file `overlays.yaml`).

Private registries: set `GITHUB_TOKEN` for ghcr.io, or mount `config.json` (via the .docker directory in your home, `DOCKER_CONFIG`, or Podman's `auth.json` under `XDG_RUNTIME_DIR/containers/`).

Example ISO with two extensions and a replaced console argument:

```sh
docker run --rm -t -v "$PWD/_out:/out" ghcr.io/siderolabs/imager:<version> iso \
  --system-extension-image <gvisor ref> --system-extension-image <intel-ucode ref> \
  --extra-kernel-arg net.ifnames=0 --extra-kernel-arg=-console --extra-kernel-arg=console=ttyS1
```

For PXE use `iso --output-kind kernel` and `--output-kind initramfs`; kernel args cannot be embedded there. Build the `installer` separately with `installer --platform=metal`, then `crane push` the tar.

## Checked

2026-11-04. Imager invocation, profiles, flags, crane lookups, registry auth and the ISO/PXE/installer examples confirmed on the Boot Assets page.

Method: documentation only; no commands were run.
