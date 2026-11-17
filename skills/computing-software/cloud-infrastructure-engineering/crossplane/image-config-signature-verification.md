---
id: computing-software.cloud-infrastructure-engineering.crossplane.image-config-signature-verification
name: image-config-signature-verification
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [imageconfig, cosign, signature, verification, supply-chain]
level: advanced
status: docs-checked
description: "Verify package signatures with Cosign through ImageConfig and read the Verified condition."
sources:
  - https://docs.crossplane.io/latest/packages/image-configs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Signature verification is alpha. Enable `--enable-signature-verification`. The package manager then verifies each matching image before pulling and rejects invalid ones.

```yaml
apiVersion: pkg.crossplane.io/v1beta1
kind: ImageConfig
metadata:
  name: verify-acme-packages
spec:
  matchImages:
  - prefix: registry1.com/acme-co/configuration-foo
  verification:
    provider: Cosign
    cosign:
      authorities:
      - name: verify acme packages
        keyless:
          identities:
          - issuer: https://token.actions.githubusercontent.com
            subject: https://github.com/acme-co/crossplane-packages/.github/workflows/supplychain.yml@refs/heads/main
        attestations:
        - name: verify attestations
          predicateType: spdxjson
```

`Cosign` is the only provider. The API mirrors Sigstore Policy Controller, with a subset of options. With several authorities, identities or attestations, one valid match is enough.

The result is a `Verified` condition on ProviderRevision, ConfigurationRevision or FunctionRevision:

- `SignatureVerificationSkipped`: no matching ImageConfig with verification.
- `VerificationSucceeded`.
- `SignatureVerificationFailed`: status False.
- `SignatureVerificationIncomplete`: error, for example a missing `cosign.pub` key in a secret.

No condition means the feature is not enabled.

Verification applies to the image matched by `matchImages`, so list each package or prefix you want checked.

## Checked

Alpha flag, Cosign provider, authority example, any-one-match rule, Verified condition reasons and the no-condition-when-disabled behaviour confirmed on the Image Configs page. An unsourced claim about packages with no matching config and a flag-reminder sentence were removed.

Method: docs-checked 2026-11-09 against the raw Image Configs page (docs repo, current content folder), read in full.
