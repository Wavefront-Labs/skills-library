---
id: computing-software.cybersecurity-defensive.cosign.signing-config-create
name: signing-config-create
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, signing-config-create, rekor-config, tsa-config, base-config, rekor-v2]
level: advanced
status: docs-checked
description: "Create a Sigstore signing config with cosign signing-config create: service specs, ANY/ALL/EXACT selection, base-config overrides and default services."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_signing-config_create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# signing-config create

```
cosign signing-config create --with-default-services --out sigstore-signing-config.json

cosign signing-config create \
    --fulcio="url=https://fulcio.sigstore.dev,api-version=1,start-time=2024-01-01T00:00:00Z,end-time=2025-01-01T00:00:00Z,operator=sigstore.dev" \
    --rekor="url=https://rekor.sigstore.dev,api-version=1,start-time=2024-01-01T00:00:00Z,operator=sigstore.dev" \
    --rekor-config="ANY" \
    --oidc-provider="url=https://oauth2.sigstore.dev/auth,api-version=1,start-time=2024-01-01T00:00:00Z,operator=sigstore.dev" \
    --tsa="url=https://timestamp.sigstore.dev/api/v1/timestamp,api-version=1,start-time=2024-01-01T00:00:00Z,operator=sigstore.dev" \
    --tsa-config="EXACT:1" \
    --out signing-config.json
```

Rules:
- Each service spec requires url, api-version (integer), start-time, operator; end-time optional.
- `--rekor-config` is required if `--rekor` is given; `--tsa-config` likewise. Values: ANY, ALL, or EXACT:count.
- `--base-config` starts from an existing file; service flags replace its services.
- `--with-default-rekor-v2` uses the TUF root with the Rekor v2 service.
- `--no-default-fulcio|oidc|rekor|tsa` remove defaults.

Use it: `cosign sign --signing-config signing-config.json ...` (see signing-config-flag).

## Checked

2026-11-04. Confirmed on the cosign signing-config create reference page: both examples, the required and optional service keys, `--rekor-config` and `--tsa-config` values and requirement, `--base-config`, `--with-default-services`, `--with-default-rekor-v2`, `--no-default-*` and `--out`; and on the sign page (`--signing-config`). Nothing needed removing.

Method: documentation only; no commands were run.
