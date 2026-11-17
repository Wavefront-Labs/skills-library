---
id: computing-software.cybersecurity-defensive.cosign.bundle-create-from-container
name: bundle-create-from-container
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, create-from-container, oci-referrers, legacy-attestations, bundle]
level: advanced
status: docs-checked
description: "Convert legacy tag-based .att attestations on an image into Sigstore bundles attached as OCI 1.1 referrers with cosign bundle create-from-container."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_bundle_create-from-container.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bundle create-from-container

Creates bundles "from attestations stored in the legacy tag-based format (.att) for a container image, and attach them to the image as OCI 1.1 referrers. Bundles that are already attached are skipped."

```
cosign bundle create-from-container <IMAGE>                        # keyless attestations
cosign bundle create-from-container --key cosign.pub <IMAGE>        # key-based attestations
```

Flags: `--key` (public key file, KMS URI or Kubernetes Secret), `--sk`, `--slot`, `--ignore-tlog`, `--rekor-url` (default `https://rekor.sigstore.dev`), plus the registry auth/TLS flags and `--k8s-keychain`.

Behaviour notes:
- It is rerunnable: already-attached bundles are skipped.
- Bundles are attached as OCI 1.1 referrers (see bundle-oci-referrers). `cosign tree <IMAGE>` lists what is attached.
- Use `--ignore-tlog` only for attestations never uploaded to Rekor.


## Checked

2026-11-04. Confirmed on the cosign bundle create-from-container reference page: the quoted description, both examples, `--key`, `--sk`, `--slot`, `--ignore-tlog`, `--rekor-url` default, registry flags and `--k8s-keychain`; and on the cosign tree page. Removed: the registry requirement wording and the remark about newer attestations using the bundle format directly.

Method: documentation only; no commands were run.
