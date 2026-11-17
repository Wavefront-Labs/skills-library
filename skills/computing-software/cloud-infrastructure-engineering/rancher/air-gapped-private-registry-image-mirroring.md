---
id: computing-software.cloud-infrastructure-engineering.rancher.air-gapped-private-registry-image-mirroring
name: air-gapped-private-registry-image-mirroring
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [air-gap, private-registry, rancher-images-txt, rancher-save-images, rancher-load-images, cert-manager-image]
level: advanced
status: docs-checked
description: "Mirror Rancher images for an air gapped install: release assets rancher-images.txt and the save/load scripts, adding the cert-manager image, and Windows differences."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/other-installation-methods/air-gapped-helm-cli-install/publish-images
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/other-installation-methods/air-gapped-helm-cli-install/infrastructure-private-registry
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default every image used to provision clusters or launch Rancher tools such as monitoring comes from Docker Hub. An air gapped install therefore needs a private registry reachable from the Rancher server, loaded with all required images. The process is the same for Docker and Kubernetes installs. If the registry has certificates, the K3s private registry documentation applies, and certs plus registry configuration must be mounted into the Rancher container.

The Linux-only flow uses a Linux workstation with internet access, access to the registry and at least 20 GB free. ARM64 hosts need a registry that supports manifests.

1. From the Rancher GitHub release (not an `rc` or pre-release), download from **Assets**: `rancher-images.txt`, `rancher-save-images.sh` and `rancher-load-images.sh`.
2. For a Kubernetes install using Rancher's self-signed certificates, add the cert-manager images to the list, then de-duplicate with `sort -u rancher-images.txt -o rancher-images.txt`.
3. Create the tarball with `./rancher-save-images.sh --image-list ./rancher-images.txt`.
4. Log in with `docker login <REGISTRY.YOURDOMAIN.COM:PORT>`, then push:

```plain
./rancher-load-images.sh --image-list ./rancher-images.txt --registry <REGISTRY.YOURDOMAIN.COM:PORT>
```

The images list and tarball must sit in the directory where you run the load script.

If Rancher will provision Windows clusters, there are separate steps: Windows images are collected from a Windows Server 1809 workstation with at least 50 GB and Docker 18.02+, and the registry must support manifests (the page notes Amazon ECR did not as of April 2020).

The infrastructure page lists the supporting pieces for an HA K3s air gap: two Linux nodes with an external datastore or three with embedded etcd, a datastore (an external PostgreSQL, MySQL or etcd database, or embedded etcd), a load balancer, a DNS record and the private registry.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Collect and Publish Images to your Private Registry; Set up Infrastructure and Private Registry. Fixed the K3s infrastructure line (two nodes with an external datastore, three with embedded etcd).

Method: documentation only; no commands were run.
