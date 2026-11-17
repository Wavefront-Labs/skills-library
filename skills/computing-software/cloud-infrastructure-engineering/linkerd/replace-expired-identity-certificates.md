---
id: computing-software.cloud-infrastructure-engineering.linkerd.replace-expired-identity-certificates
name: replace-expired-identity-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, mtls, certificates, expiry, recovery]
level: advanced
status: docs-checked
description: "Recover from an expired issuer or trust root certificate, using linkerd check output to choose between rotation and full replacement."
sources:
  - https://linkerd.io/2.19/tasks/replacing_expired_certificates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If certificates have expired, the mesh is already in an invalid state, so zero-downtime rotation is not guaranteed. Run `linkerd check --proxy` to see which certificate expired.

Issuer expired only: the check reports `issuer cert is within its validity period` as failed. If you installed with your own trust root and still have its key, follow the issuer rotation procedure in the manual rotation guide.

Root expired, or you lack the root key: the check reports `trust roots are within their validity period` as failed. You must replace both root and issuer together. Generate new ones as in the certificate generation guide, then run:

```bash
linkerd upgrade \
    --identity-issuer-certificate-file=./issuer-new.crt \
    --identity-issuer-key-file=./issuer-new.key \
    --identity-trust-anchors-file=./ca-new.crt \
    --force \
    | kubectl apply -f -
```

`upgrade` normally refuses an issuer certificate that will not work with the roots meshed pods currently use. `--force` skips that check, which is appropriate here because you are changing both at once.

While pods restart after the trust bundle update, `linkerd check --proxy` warns about pods without the current trust bundle (`data plane proxies certificate match CA`). Once those warnings clear, use `kubectl rollout restart` on your meshed workloads to bring them up to date, after which `linkerd check` should show no warnings or errors.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/tasks/replacing_expired_certificates/. Invalid-state warning, the two failing-check outputs, issuer-only versus root-and-issuer cases, the `linkerd upgrade` command with `--force` and its reason, the post-restart check behaviour.

Removed or reworded: The statement about identities issued under the old chain (not on the cited page).

Method: documentation only; no commands were run.
