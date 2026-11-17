---
id: computing-software.messaging-and-integration.dapr.mtls-certificate-rotation-kubernetes
name: mtls-certificate-rotation-kubernetes
category: computing-software
field: messaging-and-integration
product: dapr
tags: [mtls, certificate-rotation, dapr-mtls, renew-certificate, trust-bundle, sentry, downtime]
level: advanced
status: docs-checked
description: "Rotate Dapr root and issuer certificates on Kubernetes: dapr mtls renew-certificate options, clearing the dapr-trust-bundle secret, restart order, and downtime rules by key reuse."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/security/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recommended: the CLI. Generate brand-new root and issuer certs signed by a new root key (restart so services reload them):

```bash
dapr mtls renew-certificate -k --valid-until <days> --restart
```

Sign with your own root private key instead (if the deployed certs used the same key, Sentry reads them without a restart):

```bash
dapr mtls renew-certificate -k --private-key <private_key_file_path> --valid-until <days>
```

Replace with custom certs (`--valid-until` is not supported here):

```bash
dapr mtls renew-certificate -k --ca-root-certificate <ca.crt> --issuer-private-key <issuer.key> --issuer-public-certificate <issuer.crt> --restart
```

Whichever you use, restart every Dapr-enabled pod (`kubectl rollout restart deploy/myapp`); expect some downtime until all have reloaded.

Manual rotation of Dapr-generated certs: apply an empty `dapr-trust-bundle` secret (labelled `app: dapr-sentry`, empty `data:`), restart `deployment/dapr-sentry`, then restart `dapr-operator`, `dapr-placement-server` (statefulset), `dapr-sidecar-injector`, `dapr-scheduler-server`, then your apps. Service invocation between apps fails until the callee has restarted too, and placement cannot assign new actors meanwhile.

Custom certs: `helm upgrade` with the `--set-file dapr_sentry.tls...` flags, or `kubectl edit secret dapr-trust-bundle -n <DAPR_NAMESPACE>` replacing the base64 values of `ca.crt`, `issuer.crt` and `issuer.key`. If the new root uses the same private key, Sentry picks it up automatically and app restarts are zero-downtime; with a different key, restart Sentry first, then operator and placement, then all apps.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
