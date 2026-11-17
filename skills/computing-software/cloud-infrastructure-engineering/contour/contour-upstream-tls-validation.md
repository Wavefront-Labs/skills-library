---
id: computing-software.cloud-infrastructure-engineering.contour.contour-upstream-tls-validation
name: contour-upstream-tls-validation
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [upstream-tls, upstream-protocol, validation, casecret, subjectnames, caching, envoy-client-certificate]
level: advanced
status: docs-checked
description: "Proxying to TLS backends: upstream-protocol.tls annotation or services[].protocol, validation caSecret/subjectNames, invalid-status behaviour, Envoy client certificate."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/upstream-tls.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upstream TLS and validation

To make Envoy speak TLS to a backend, either annotate the Service with `projectcontour.io/upstream-protocol.tls: "8443"` (port list) or set `protocol: tls` on `spec.routes[].services[]`. If both are set, the `protocol` field wins.

By default the upstream server certificate is not validated. Request validation with:

```yaml
routes:
- services:
  - name: secure-backend
    port: 8443
    validation:
      caSecret: my-certificate-authority
      subjectName: backend.example.com
      subjectNames:
      - backend.example.com
      - alt.example.com
```

- `caSecret` is an Opaque Secret with a PEM bundle under `ca.crt`; `ns/name` form needs TLS certificate delegation.
- `subjectName` is deprecated (250 char limit) in favour of `subjectNames`; the first `subjectNames` entry must equal `subjectName`.
- When `validation` is present, the Service must carry the matching `upstream-protocol.tls` annotation (the annotation goes on the Service, not on the Ingress or HTTPProxy).
- If the referenced Secret is missing, Contour rejects the update and sets the HTTPProxy status to `invalid` with a message like `upstreamValidation requested but secret not found or misconfigured`.

Mutual TLS to the backend: set the `namespace/name` of a Kubernetes Secret in the Contour configuration file as the Envoy client certificate. Envoy sends that certificate during the TLS handshake when the backend asks for one, letting the application verify the connection came from Envoy.

## Checked

2026-11-08. Read the Contour main-branch config page upstream-tls.md in full. Confirmed: annotation and `protocol` field with the field taking precedence, no validation by default, `caSecret` Secret type and `ca.crt` key, delegation for cross-namespace CA Secrets, deprecated `subjectName` with its 250 character limit and the first-entry rule, the annotation requirement when `validation` is set, the invalid status on a missing Secret, and the Envoy client certificate. Removed the `tls.envoy-client-certificate` and `cluster.upstream-tls` key names, which this page does not give.

Method: documentation only; no commands were run.
