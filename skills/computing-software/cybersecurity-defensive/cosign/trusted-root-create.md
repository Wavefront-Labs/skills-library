---
id: computing-software.cybersecurity-defensive.cosign.trusted-root-create
name: trusted-root-create
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, trusted-root-create, trusted-root, fulcio, rekor, ctfe, tsa]
level: advanced
status: docs-checked
description: "Build a Sigstore TrustedRoot JSON for a private deployment with cosign trusted-root create, service key-value specs, defaults and validity times."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_trusted-root_create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# trusted-root create

Each service is a repeatable flag taking comma-separated key-value pairs.

```
cosign trusted-root create \
    --fulcio="url=https://fulcio.sigstore.dev,certificate-chain=/path/to/fulcio.pem,end-time=2025-01-01T00:00:00Z" \
    --rekor="url=https://rekor.sigstore.dev,public-key=/path/to/rekor.pub,start-time=2024-01-01T00:00:00Z" \
    --ctfe="url=https://ctfe.sigstore.dev,public-key=/path/to/ctfe.pub,start-time=2024-01-01T00:00:00Z" \
    --tsa="url=https://timestamp.sigstore.dev/api/v1/timestamp,certificate-chain=/path/to/tsa.pem" \
    --out trusted-root.json
```

Required keys:
- `--fulcio`, `--tsa`: url, certificate-chain (PEM chain path). Optional start-time, end-time.
- `--rekor`, `--ctfe`: url, public-key (PEM path), start-time. Optional end-time, origin.

Defaults: `--with-default-services` fills from the Sigstore TUF root; service flags override. `--no-default-ctfe|fulcio|rekor|tsa` remove default URLs.

Use the result: `cosign verify --trusted-root trusted-root.json ...`.

Gotchas:
- Times are written as in the example, for instance `2025-01-01T00:00:00Z`.
- Pair with a signing config for the signing side (signing-config-create).

## Checked

2026-11-04. Confirmed on the cosign trusted-root create reference page: the example, required and optional keys per service, `--with-default-services`, `--no-default-*`, `--out`; and on the verify page (`--trusted-root`). Removed: the advice about giving old keys an end-time and the RFC 3339 label.

Method: documentation only; no commands were run.
