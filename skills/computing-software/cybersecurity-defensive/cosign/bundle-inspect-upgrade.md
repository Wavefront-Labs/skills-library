---
id: computing-software.cybersecurity-defensive.cosign.bundle-inspect-upgrade
name: bundle-inspect-upgrade
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, bundle-inspect, bundle-upgrade, sigstore-bundle]
level: practitioner
status: docs-checked
description: "Inspect a Sigstore bundle and upgrade it to the latest bundle version with cosign bundle inspect and bundle upgrade."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_bundle_inspect.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_bundle_upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bundle inspect and upgrade

```
cosign bundle inspect BUNDLE
cosign bundle upgrade <bundle> --out upgraded.sigstore.json
```

`inspect` takes just the bundle path and no other options.

`upgrade`: "Upgrade a Sigstore Protobuf bundle to the latest version. This command only supports standardized bundles."
- `--out`: path of the output upgraded bundle file.
- `--rekor-url`: URL of the transparency log, default `https://rekor.sigstore.dev`.

Notes:
- Non-standard (old format) bundles are converted with `bundle create --bundle` instead (see bundle-create).
- The OCI bundle media type in the spec is `application/vnd.dev.sigstore.bundle.v0.3+json`; `verify` has `--allow-certificate-chain` for v0.3+ bundles.

## Checked

2026-11-04. Confirmed on the cosign bundle inspect and bundle upgrade reference pages (usage lines, `--out`, `--rekor-url` default, the quoted upgrade description), the bundle create page (`--bundle` old format) and the bundle spec (media type v0.3) and verify page (`--allow-certificate-chain`). Removed: what inspect shows, and the guess that upgrade queries the log.

Method: documentation only; no commands were run.
