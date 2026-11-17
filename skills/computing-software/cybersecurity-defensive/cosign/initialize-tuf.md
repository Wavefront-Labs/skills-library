---
id: computing-software.cybersecurity-defensive.cosign.initialize-tuf
name: initialize-tuf
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, initialize, tuf, staging, mirror, root-checksum, trusted-root]
level: advanced
status: docs-checked
description: "Use cosign initialize to fetch the Sigstore TUF root, staging repo, custom mirror, out-of-band root with checksum, and air-gap file mirror."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_initialize.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign initialize

Defaults: the current trusted Sigstore TUF root is embedded in cosign at release time; the remote TUF repo comes from the CDN mirror at `tuf-repo-cdn.sigstore.dev`. Updated TUF data is written to `$HOME/.sigstore/root/`. Trusted keys and certificates for verification (for example the Fulcio root CA) come from this metadata.

```
cosign initialize
cosign initialize --staging
cosign initialize --root <url>
cosign initialize --mirror <url> --root <url> --root-checksum <sha256>
```

Flags:
- `--mirror`: "GCS bucket to a SigStore TUF repository, or HTTP(S) base URL, or file:/// for local filestore remote (air-gap)".
- `--root`: path or URL to a trusted initial root.json instead of the embedded one.
- `--root-checksum`: required if the root is downloaded via http(s); sha256 by default, or `sha512:<checksum>`.
- `--staging`: staging repository.

Gotchas:
- `--root-checksum` is required when the root is downloaded via http(s).
- Air-gapped hosts: initialize while online, then refresh deliberately (the README warns the trusted_root.json "will change without notification").
- Default trusted root path in the README: `~/.sigstore/root/tuf-repo-cdn.sigstore.dev/targets/trusted_root.json`.

## Checked

2026-11-04. Confirmed on the cosign initialize reference page (defaults, `$HOME/.sigstore/root/`, examples, `--mirror`, `--root`, `--root-checksum` with sha512 option, `--staging`) and in the README air-gapped section (trusted_root.json path and the change-without-notification warning). Removed: the generic advice about fetching over a checksummable channel.

Method: documentation only; no commands were run.
