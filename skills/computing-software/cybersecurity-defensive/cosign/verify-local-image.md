---
id: computing-software.cybersecurity-defensive.cosign.verify-local-image
name: verify-local-image
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, local-image, verify, offline, air-gap]
level: practitioner
status: docs-checked
description: "Verify a signed image saved to disk with cosign verify --local-image, for keyed and keyless cases and the README's offline caveats."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verify a locally saved image

`--local-image`: "whether the specified image is a path to an image saved locally via 'cosign save'".

```
cosign save $IMAGE_NAME --dir ./path/to/dir      # online step
cosign verify --key cosign.pub --local-image ./path/to/dir
```

Keyless version in the README (marked "out of date" there):

```
cosign verify \
  --certificate-identity $CERT_IDENTITY \
  --certificate-oidc-issuer $CERT_OIDC_ISSUER \
  --offline=true \
  --new-bundle-format=false \
  --trusted-root ~/.sigstore/root/tuf-repo-cdn.sigstore.dev/targets/trusted_root.json \
  --local-image ./path/to/dir
```

Notes:
- The README says `--new-bundle-format=false` is for artifacts signed without the new protobuf bundle format. Those `--offline` and `--new-bundle-format` flags are not in the current verify page, so check `cosign verify --help` for your version.
- Run `cosign initialize` while online to fetch the TUF root.
- The trusted root changes without notice; air-gapped copies need their own refresh process.

Also works for `verify-attestation --local-image`.

## Checked

2026-11-04. Confirmed in the cosign README (air-gapped section, marked out of date: the keyless example, `--new-bundle-format=false` comment, `cosign initialize` and `cosign save` steps, trusted root changes without notification) and on the cosign verify, verify-attestation and save reference pages (`--local-image`, `--dir`). The keyed README example uses `--offline`, which is not on the current verify page.

Method: documentation only; no commands were run.
