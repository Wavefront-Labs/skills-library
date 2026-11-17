---
id: computing-software.cybersecurity-defensive.cosign.tree-artifacts
name: tree-artifacts
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, tree, referrers-mode, supply-chain, inventory]
level: practitioner
status: docs-checked
description: "List signatures, attestations and SBOMs attached to an image with cosign tree, and choose legacy or oci-1-1 referrers discovery."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_tree.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign tree

"Display supply chain security related artifacts for an image such as signatures, SBOMs and attestations."

```
cosign tree <IMAGE>
cosign tree --registry-referrers-mode oci-1-1 <IMAGE>
```

- `--registry-referrers-mode`: "mode for fetching references from the registry. allowed: legacy, oci-1-1". - Registry auth/TLS flags and `--k8s-keychain` apply.
- `cosign sign` has the same referrers-mode flag.

Tree lists artifacts, it does not verify them. Run `cosign verify` for trust.

## Checked

2026-11-04. Confirmed on the cosign tree and cosign sign reference pages: the description quote, `cosign tree <IMAGE>`, `--registry-referrers-mode` with allowed values legacy and oci-1-1 (also on sign), and the registry auth, TLS and `--k8s-keychain` flags. Removed: the explanation of what legacy and oci-1-1 mean, the use-case list and the advice about disagreeing registries (not on the pages).

Method: documentation only; no commands were run.
