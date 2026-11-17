---
id: computing-software.devops-ci-cd.flux.ocirepository-signature-verification
name: ocirepository-signature-verification
category: computing-software
field: devops-ci-cd
product: flux
tags: [ocirepository, cosign, notation, keyless, verify]
level: advanced
status: docs-checked
description: "Verify OCI artifact signatures with Cosign keys, Cosign keyless OIDC identity matchers, or Notation."
sources:
  - https://fluxcd.io/flux/components/source/ocirepositories/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.verify` on an OCIRepository checks signatures before the artifact is used. Subfields:
- `provider`: `cosign` or `notation`.
- `secretRef.name`: Secret with Cosign public keys, or for Notation the trust policy plus CA certificate.
- `matchOIDCIdentity`: OIDC identity matchers, cosign only.

Key-based Cosign: put the public keys in a Secret in the same namespace. Keys must have the `.pub` extension:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cosign-pub
type: Opaque
data:
  key1.pub: <BASE64>
```

```yaml
spec:
  verify:
    provider: cosign
    secretRef:
      name: cosign-pub
```

Keyless: omit `secretRef` and match the Fulcio certificate identity. Matchers are Go regexps evaluated as OR; `issuer` matches the OIDC issuer, `subject` the identity:

```yaml
spec:
  verify:
    provider: cosign
    matchOIDCIdentity:
      - issuer: "^https://token.actions.githubusercontent.com$"
        subject: "^https://github.com/org/repo.*$"
```

By default the Fulcio root CA and the Rekor instance at rekor.sigstore.dev are used. For a self-hosted Sigstore deployment, or to pin a trust root, supply a Sigstore `trusted_root.json` through `.spec.verify.trustedRootSecretRef`.

On success a `SourceVerified` condition with status `True` and reason `Succeeded` is added to `.status.conditions`.

## Checked

2026-11-03. Read the OCIRepository reference (fluxcd.io/flux/components/source/ocirepositories/): `verify` subfields, `.pub` key suffix, keyless `matchOIDCIdentity` (Go regexps, OR evaluation), default Fulcio and rekor.sigstore.dev, `trustedRootSecretRef` for self-hosted Sigstore, and the SourceVerified condition. Removed the claims that keyless is experimental and that custom roots are unsupported (the page now documents them), the unconfirmed cosign CLI commands and an advice line.

Method: documentation only; no commands were run.
