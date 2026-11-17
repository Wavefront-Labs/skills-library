---
id: computing-software.cloud-infrastructure-engineering.istio.istio-plugin-ca-certificates
name: istio-plugin-ca-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, plugin-ca, cacerts, root-ca]
level: practitioner
status: docs-checked
description: "Replace the self-signed Istio root with an organisational intermediate by creating the cacerts secret before first install."
sources: ["https://istio.io/latest/docs/tasks/security/cert-management/plugin-ca-cert/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Provide a plugged-in CA to istiod through a `cacerts` secret in `istio-system`. The Istio task is demo-only and recommends a production-ready CA such as HashiCorp Vault for production, with the root CA managed on an offline machine.

```sh
kubectl create namespace istio-system
kubectl create secret generic cacerts -n istio-system \
  --from-file=ca-cert.pem --from-file=ca-key.pem \
  --from-file=root-cert.pem --from-file=cert-chain.pem
istioctl install --set profile=demo
```

Gotchas: the secret holds `ca-cert.pem` (intermediate certificate), `ca-key.pem` (intermediate key), `root-cert.pem` (root) and `cert-chain.pem` (the chain used by istiod). On the page, the self-signed example CA makes `openssl` report `verify error:num=19:self signed certificate in certificate chain`, which is expected.

Verify: retrieve a workload certificate chain and check it against the plugged-in CA, following the task: `openssl verify -CAfile <(cat ca-cert.pem root-cert.pem) ./proxy-cert-1.pem`.

## Checked

2026-11-03. Confirmed in the Istio plug-in CA certificates task: the `cacerts` secret in `istio-system` with the four file names, the demo-only warning, offline root advice, and the `openssl verify` form. Removed: the self-signed default claim, the must-exist-before-first-start and root-change rollout claims, `istioctl proxy-config secret ... deploy/web.shop`, the `-CAfile root-cert.pem`-only verify form and the rotation-runbook advice (not on the page).

Method: documentation only; no commands were run.
