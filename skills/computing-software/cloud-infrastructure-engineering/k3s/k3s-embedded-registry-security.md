---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-embedded-registry-security
name: k3s-embedded-registry-security
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, spegel-security, latest-tag, image-digest]
level: sme
status: docs-checked
description: "Security model and caveats of the K3s embedded registry mirror: trust, credentials leakage, tag poisoning, latest tag."
sources:
  - https://docs.k3s.io/installation/registry-mirror
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authentication: access to the mirror registry API needs a client certificate signed by the cluster client CA. Access to the peer-to-peer network needs a preshared key controlled by server nodes. Nodes authenticate each other with both the key and a cluster-CA certificate.

Warning: the design assumes equal privilege and trust between all cluster members. If that does not match your security posture, do not enable it.

Concerns listed in the docs:

- It may expose images a node could not otherwise access. If some images need Kubernetes image pull secrets or credentials in registries.yaml, other nodes can get them from peers without presenting any credentials upstream.
- Anyone able to push images into the containerd store on one node may poison a tag for other nodes, which trust the advertised tag without checking upstream. If integrity matters, use image digests instead of tags, since a digest cannot be poisoned this way.

Latest tag: images without a tag default to latest, which moves over time. The distributed registry does not pull latest from other nodes; containerd goes to an upstream registry or mirror, matching Kubernetes defaulting of imagePullPolicy for latest. Setting the K3S_P2P_ENABLE_LATEST=true environment variable on the service enables mirroring latest, but it is unsupported and not recommended.

Sharing is by source registry: manually loaded images are shared only if tagged as from a registry enabled for mirroring, and that registry need not exist or be reachable.

## Checked

2026-11-08. Read the full K3s Embedded Registry Mirror page (docs/installation/registry-mirror.md in the k3s-io/docs repo). Confirmed: client certificate and preshared key authentication, the equal-trust warning, credential exposure, tag poisoning and the digest advice, latest tag behaviour and K3S_P2P_ENABLE_LATEST, and sharing by source registry. Nothing removed.

Method: documentation only; no commands were run.
