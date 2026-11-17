---
id: computing-software.cloud-infrastructure-engineering.linkerd.generate-mtls-trust-anchor-and-issuer
name: generate-mtls-trust-anchor-and-issuer
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, mtls, certificates, step, trust-anchor]
level: advanced
status: docs-checked
description: "Generate an ECDSA P-256 trust anchor and issuer certificate with step and pass them to linkerd install or Helm."
sources:
  - https://linkerd.io/2.19/tasks/generate-certificates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd needs a trust anchor certificate and an issuer certificate with its key for mTLS. `linkerd install` generates them if you do not supply any, but with Helm you must provide your own. All certificates must use ECDSA P-256, which is the default for `step`; with openssl use `openssl ecparam -name prime256v1`.

Trust anchor:

```bash
step certificate create root.linkerd.cluster.local ca.crt ca.key \
--profile root-ca --no-password --insecure
```

Add `--not-after=87600h` for a longer-lived anchor. Issuer, signed by the anchor:

```bash
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key \
--profile intermediate-ca --not-after 8760h --no-password --insecure \
--ca ca.crt --ca-key ca.key
```

Install with the CLI, CRDs first:

```bash
linkerd install --crds | kubectl apply -f -
linkerd install \
  --identity-trust-anchors-file ca.crt \
  --identity-issuer-certificate-file issuer.crt \
  --identity-issuer-key-file issuer.key \
  | kubectl apply -f -
```

With Helm, install `linkerd-crds`, then pass `ca.crt` as `identityTrustAnchorsPEM` and the issuer files as `identity.issuer.tls.crtPEM` and `identity.issuer.tls.keyPEM` to `linkerd-control-plane`.

`--no-password --insecure` avoids encrypting the files with a passphrase.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/generate-certificates/.

Removed or reworded: Storage advice not on the page.

Method: documentation only; no commands were run.
