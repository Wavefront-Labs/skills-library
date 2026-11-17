---
id: computing-software.devops-ci-cd.argocd-image-updater.cosign-signature-verification
name: cosign-signature-verification
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, cosign, image-signature, imagesverification, supply-chain, public-key, referrers-api, application-refs]
level: advanced
status: docs-checked
description: "Verify cosign signatures before updating: sign by digest, store the public key in a Secret, set imagesVerification at global, application or image level, and opt images out."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/applications.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cosign signature verification

When configured, an update is applied only if the image has a valid signature from the configured key; failures are skipped and logged.

Sign by digest (not tag) so the signature stays valid if the tag moves:

```shell
cosign generate-key-pair
cosign sign --key cosign.key <registry>/<repo>@<digest>
cosign verify --key cosign.pub <registry>/<repo>@<digest>
```

Store the public key in a Secret in the same namespace as the CR:

```shell
kubectl create secret generic myapp-cosign-pubkey \
  --from-file=cosign.pub=./cosign.pub -n argocd
```

Configure with `imagesVerification` at top level, `applicationRefs[]`, or per image; more specific scopes override, absent fields inherit:

```yaml
spec:
  imagesVerification:
    cosignKey:
      secretName: org-cosign-pubkey
      key: cosign.pub
  applicationRefs:
    - namePattern: "my-app"
      images:
        - alias: "nginx"
          imageName: "nginx:~1.26"
          imagesVerification:
            enabled: false     # opt this image out
```

Facts: only cosign key-based verification is supported (ECDSA public key); signatures are found via the OCI Referrers API, falling back to the `sha256-<digest>` tag on older registries. `enabled` defaults to `true`, and then `cosignKey` (`secretName` and `key`) is required or the image is skipped with an error. With no `imagesVerification` block, images update unverified.

## Checked

2026-11-04. Confirmed against images.md (Image Signature Verification: signing by digest, Secret creation, CR examples, opt-out, Referrers API fallback, field table with enabled default true and cosignKey secretName/key) and applications.md (imagesVerification on applicationRefs).

Method: documentation only; no commands were run.
