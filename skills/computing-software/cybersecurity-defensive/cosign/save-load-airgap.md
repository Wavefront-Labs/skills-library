---
id: computing-software.cybersecurity-defensive.cosign.save-load-airgap
name: save-load-airgap
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, save, load, air-gap, offline, local-image]
level: advanced
status: docs-checked
description: "Move a signed image and its signatures to an air-gapped registry with cosign save and cosign load, then verify offline with the matching trusted root."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_save.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_load.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Save and load

```
cosign save --dir /path/to/dir <IMAGE>        # image plus associated signatures to disk
cosign load --dir /path/to/dir <IMAGE>        # push a saved signed image to a registry
```

Flags: `--dir` (directory), registry auth/TLS, `--k8s-keychain`.

Air-gapped flow (README, flagged "out of date"):
1. Online: `cosign initialize` (pulls the latest TUF root), then `cosign save $IMAGE_NAME --dir ./path/to/dir`.
2. Offline: `cosign verify ... --local-image ./path/to/dir` (see verify-local-image), or load into an internal registry and verify there.

Facts:
- Keyless signing includes the bundle annotation by default, so the default `cosign sign` output has the material for offline verification.
- The trusted root (`trusted_root.json`) must be copied too and kept current; it "will change without notification" and without TUF you need your own update mechanism.
- If you signed with a key, `cosign verify --key cosign.pub --offline --local-image ./path/to/dir` works with the public key present locally.

Always pass identity and issuer for keyless images.

## Checked

2026-11-04. Confirmed on the cosign save and load reference pages (descriptions, `--dir`, registry flags, `--k8s-keychain`) and in the README air-gapped section (marked out of date: the initialize and save steps, bundle annotation included by default for keyless signing, trusted root changes without notification, the keyed example with `--offline`). Removed: the word required for `--dir`.

Method: documentation only; no commands were run.
