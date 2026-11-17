---
id: computing-software.cloud-infrastructure-engineering.istio.istio-workload-certificates-sds
name: istio-workload-certificates-sds
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, workload-certificates, spiffe, sds]
level: practitioner
status: docs-checked
description: "Check SPIFFE identity, issuer and expiry of workload certificates with istioctl, and diagnose expired-cert mTLS failures."
sources: ["https://istio.io/latest/docs/ops/common-problems/security-issues/", "https://istio.io/latest/docs/tasks/security/authorization/authz-http/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each workload certificate carries a SPIFFE identity as a URI Subject Alternative Name, of the form `spiffe://cluster.local/ns/<ns>/sa/<sa>`.

```sh
istioctl proxy-config secret deploy/web.shop
istioctl proxy-config secret deploy/web.shop -o json | \
  jq -r '[.dynamicActiveSecrets[] | select(.name == "default")][0].secret.tlsCertificate.certificateChain.inlineBytes' | \
  base64 -d | openssl x509 -noout -text
```

Gotchas: authorization `principals` use the identity string without the `spiffe://` prefix (for example `cluster.local/ns/default/sa/bookinfo-productpage`). For mutual TLS problems, the Istio troubleshooting page says to first ensure istiod is healthy, then that keys and certificates are delivered to sidecars, then that the right authentication policy and DestinationRules are in place.

Verify: the certificate's Subject Alternative Name is `URI:spiffe://cluster.local/ns/<ns>/sa/<sa>`, and the `Not After` validity date is in the future.

## Checked

2026-11-03. Confirmed in the Istio security-problems page (`istioctl proxy-config secret`, the `select(.name == "default")` jq filter, `openssl x509 -noout -text`, the SPIFFE SAN, the mutual TLS troubleshooting order) and the HTTP authorization task (`principals` form). Removed: the short-lived and automatic SDS rotation claim, the `-subject -enddate -ext subjectAltName` options, the istiod-outage expiry and service-account-change claims, and the alerting and connection-lifetime advice (not on the pages read).

Method: documentation only; no commands were run.
