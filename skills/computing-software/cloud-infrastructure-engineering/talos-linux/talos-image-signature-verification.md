---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-image-signature-verification
name: talos-image-signature-verification
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [imageverificationconfig, cosign, keyless, supply-chain, image-signatures, policy, air-gapped]
level: advanced
status: docs-checked
description: "Machine-wide image signature policy on Talos with ImageVerificationConfig: ordered rules, keyless cosign issuer/subject, deny and skip rules, and the verified label."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/security/verifying-image-signatures.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos can verify signatures on every image pull on the machine: those made by Talos itself (such as `ghcr.io/siderolabs/kubelet`) and by Kubernetes for workloads. The policy is the `ImageVerificationConfig` document, a top-down list of rules where the first match wins. A rule matches the image reference without tag or digest (for `ghcr.io/siderolabs/kubelet:v1.36.1` it matches `ghcr.io/siderolabs/kubelet`). Unmatched images are allowed by default.

Starting policy covering Talos's own images:

```yaml
apiVersion: v1alpha1
kind: ImageVerificationConfig
rules:
    - image: registry.k8s.io/*
      keyless:
        issuer: https://accounts.google.com
        subject: krel-trust@k8s-releng-prod.iam.gserviceaccount.com
    - image: ghcr.io/siderolabs/*
      keyless:
        issuer: https://accounts.google.com
        subjectRegex: '(@siderolabs\.com$|^releasemgr-svc@talos-production\.iam\.gserviceaccount\.com$)'
    - image: factory.talos.dev/*
      keyless:
        issuer: https://accounts.google.com
        subject: image-factory-signing@talos-production.iam.gserviceaccount.com
```

Make it closed by ending with a deny-all rule:

```yaml
    - image: "*"
      deny: true
```

Exempt unsigned images with `skip: true` placed before the broader rule (the docs example skips `registry.k8s.io/e2e-test-images/*`).

Two verification mechanisms, both cosign-based: keyless (issuer and subject claims; needs access to the TUF repository, so it does not work on air-gapped clusters) and public keys (no such limit, but you manage the keys and distribute the public ones).

The policy applies at pull time only; images already in the local store are not re-verified. Confirm with the `talos.dev/verified` label: `talosctl image ls` for Kubernetes images and `talosctl image ls --namespace system` for images pulled by Talos.

## Checked

2026-11-04. Rule semantics, example documents, air-gap limitation and image label check confirmed on the Verifying Image Signatures page.

Method: documentation only; no commands were run.
