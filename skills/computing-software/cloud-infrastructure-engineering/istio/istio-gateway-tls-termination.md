---
id: computing-software.cloud-infrastructure-engineering.istio.istio-gateway-tls-termination
name: istio-gateway-tls-termination
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, gateway-tls, tls-termination, gateway-credential]
level: practitioner
status: docs-checked
description: "Terminate HTTPS at the Istio ingress gateway with a Kubernetes TLS secret in the gateway namespace, and avoid the SDS secret-not-found trap."
sources: ["https://istio.io/latest/docs/tasks/traffic-management/ingress/secure-ingress/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add an HTTPS server with `tls.mode: SIMPLE` and a `credentialName` that names a Kubernetes TLS secret.

```yaml
servers:
- port: {number: 443, name: https, protocol: HTTPS}
  hosts: ["web.example.com"]
  tls: {mode: SIMPLE, credentialName: web-cert}
```

```sh
kubectl create -n istio-system secret tls web-cert --cert=tls.crt --key=tls.key
```

Gotchas: `credentialName` must be the same as the secret's name, and the guide creates the secret in `istio-system`. For mutual TLS set `mode: MUTUAL` and hold the CA certificate under the `ca.crt` key of the secret, or reference a separate secret with `caCertCredentialName`, which takes precedence. A TLS secret needs the keys `tls.key` and `tls.crt`.

Verify: `curl -v --resolve web.example.com:443:$INGRESS_HOST https://web.example.com/` completes the handshake with the expected certificate.

## Checked

2026-11-03. Confirmed in the Istio secure ingress task: `tls.mode: SIMPLE` with `credentialName` equal to the secret name, `kubectl create -n istio-system secret tls`, the MUTUAL mode with `ca.crt`, `caCertCredentialName` precedence, and the `tls.key`/`tls.crt` key names. Removed: the same-namespace-as-workload rule, the dynamic rotation claim, the `istioctl proxy-config secret` check and the cert-manager advice (not on the page).

Method: documentation only; no commands were run.
