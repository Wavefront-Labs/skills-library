---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-airgap-upgrade
name: k3s-airgap-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, airgap-upgrade, k3s-upgrade-image, system-upgrade-controller]
level: advanced
status: docs-checked
description: "Upgrade K3s in an air gap manually, or stage rancher/k3s-upgrade and system-upgrade-controller images for automated upgrades."
sources:
  - https://docs.k3s.io/installation/airgap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Manual upgrade procedure:

1. Download the new airgap images tar for the target version and place it in /var/lib/rancher/k3s/agent/images/ on each node. Delete the old tar.
2. Replace the K3s binary in /usr/local/bin on each node.
3. Copy over the current install script from get.k3s.io, since it may have changed.
4. Run the script again with the same environment variables as before.
5. Restart the K3s service if the installer did not.

Automated upgrade: ensure the required images are in your private registry:

- rancher/k3s-upgrade at the version you will upgrade to. The tag replaces the + in the K3s release with a -, because Docker images do not support +.
- the system-upgrade-controller and kubectl versions named in the system-upgrade-controller manifest YAML you will deploy. For example, release v0.15.2 of the controller lists rancher/system-upgrade-controller:v0.15.2 and rancher/kubectl:v1.30.3.

Check the latest controller release and download its system-upgrade-controller.yaml to read the exact versions, push the three images to your registry, then follow the automated upgrades guide.

## Checked

2026-11-08: read the whole Upgrading section of the air-gap install page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/installation/airgap). Confirmed the manual steps, the + to - tag rule, and the v0.15.2 controller and kubectl image example.

Method: documentation only; no commands were run.
