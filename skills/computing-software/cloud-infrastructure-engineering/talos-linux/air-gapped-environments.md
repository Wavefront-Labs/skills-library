---
id: computing-software.cloud-infrastructure-engineering.talos-linux.air-gapped-environments
name: air-gapped-environments
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [air-gapped, offline, registry-mirror, discovery-service, ntp, image-factory]
level: advanced
status: docs-checked
description: "Plan an air-gapped Talos install: the four recurring problems (NTP, images, Image Factory, discovery) and which feature addresses each, including PTP and a self-hosted discovery."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/platform-specific-installations/air-gapped.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/images-container-runtime/image-cache.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In a fully air-gapped environment four things usually break:

1. **Time sync.** NTP servers must be reachable internally. In virtual environments the hypervisor may provide time through its PTP interface, which needs no network access. Custom DNS and NTP server settings may also be needed.
2. **Container images.** This includes the Talos `installer`, `etcd`, `kubelet` and the Kubernetes control plane images. Redirect all pulls to an internal registry pre-populated with them, using the registry mirrors feature, or bundle them with the image cache feature. For the cache, add `talosctl images talos-bundle <version>` output to the list of images; the minimum for installing Talos are the `installer` and `installer-base` images, and including the whole bundle makes the installation media much larger.
3. **Image Factory.** Updates and installs normally use factory.talos.dev. Run an Image Factory internally; it needs private OCI registries for schematics and cached assets, a public-readable registry for `installer` images, and an ECDSA P-256 signing key.
4. **Discovery service.** By default clusters use the public service at `discovery.talos.dev`. Run a self-hosted instance (a licence from Sidero Labs is required).

With only partial connectivity most of this can be met by a pull-through cache plus HTTP proxy settings instead.

## Checked

2026-11-04. The four challenges and their remedies confirmed on the Air-gapped Environments page; image-list guidance and bundle size warning on the Image Cache page; Image Factory registry requirements on the Image Factory page.

Method: documentation only; no commands were run.
