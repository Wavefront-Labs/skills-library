---
id: computing-software.cybersecurity-defensive.cosign.sign-by-digest
name: sign-by-digest
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, sign-by-digest, cosign-sign, digest, container-image]
level: intro
status: docs-checked
description: "Sign a container image with cosign sign using its digest, not a tag, so you sign exactly what you mean to; covers keyless, local key and the basic flags."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sign an image by digest

Always sign `registry/repo@sha256:...`, not `:latest`. The docs warn that signing by tag risks races or malicious tampering, so you may sign something other than what you think.

```
cosign sign <IMAGE DIGEST>                      # Sigstore OIDC flow (keyless)
cosign sign --key cosign.key <IMAGE DIGEST>     # local key pair
cosign sign --key env://[ENV_VAR] <IMAGE DIGEST>
```

Keyless is the default: cosign generates ephemeral keys, gets a certificate from Fulcio after OIDC login, records an entry in the Rekor transparency log, then pushes the signature to the registry next to the image.

Useful flags:
- `-y, --yes` skips confirmation prompts for non-destructive operations.
- `--upload=false` does not push the signature.
- `-t, --timeout` defaults to 3m0s.
- `-d, --verbose` logs debug output.

The keyless prompt warns that the signing identity (for example your email address) is stored permanently in transparency logs.

Verify afterwards with `cosign verify` (see verify-keyless-identity or verify-with-public-key).

## Checked

2026-11-04. Confirmed on the cosign sign reference page (digest warning, examples, `--upload`, `-y`, inherited `-t` and `-d`) and in the README keyless walkthrough (ephemeral keys, Fulcio certificate, Rekor entry, signature pushed to the registry, permanent storage prompt). Removed: the CI remark, the "cannot be removed" wording and the advice on resolving tags.

Method: documentation only; no commands were run.
