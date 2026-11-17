---
id: computing-software.cybersecurity-defensive.cosign.upload-blob-artifacts
name: upload-blob-artifacts
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, upload-blob, wasm, tekton, ebpf, oci-artifacts]
level: practitioner
status: docs-checked
description: "Publish and sign non-image artifacts in an OCI registry: cosign upload blob, WASM modules, Tekton bundles, eBPF and oras pushes, signed by digest."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing other artifacts

Cosign signs anything stored as a manifest in a registry.

Blobs:
```
BLOB_URI_DIGEST=$(cosign upload blob -f artifact $BLOB_URI)
cosign sign --key cosign.key $BLOB_URI_DIGEST
```
The upload prints the direct URL (`/v2/<name>/blobs/sha256:<sum>`), so users can fetch it with curl and check the digest. README examples use the ttl.sh registry.

Others:
- WASM: `cosign upload wasm -f hello.wasm REPO/wasm`, then sign the digest (the README text says `cosign wasm upload`; its example uses `upload wasm`).
- Tekton bundles: push with `tkn bundle push`, sign the digest with cosign.
- eBPF: build and push with `bee`, sign, then verify with `--key cosign.pub`.
- OCI artifacts: `oras push`, then `cosign sign --key ... REPO/artifact@sha256:...` and `cosign verify`.

Verify the artifact with the usual `cosign verify`; the output reports claims validated and signature checked against the key.

Gotcha: as ever, sign the digest printed by the upload, not a tag, and note that only "manifests" can be signed.

Helm charts and other OCI-stored types work the same way.

## Checked

2026-11-08. Read in full: the cosign README (raw, sigstore/cosign), sections Working with Other Artifacts (Blobs, Tekton Bundles, WASM, eBPF), OCI Artifacts, Signing subjects and Other Types. Confirmed every command and the "manifests" limit.

Method: documentation only; no commands were run.
