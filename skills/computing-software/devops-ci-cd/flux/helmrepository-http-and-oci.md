---
id: computing-software.devops-ci-cd.flux.helmrepository-http-and-oci
name: helmrepository-http-and-oci
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrepository, helm, oci, passcredentials, secretref]
level: sme
status: docs-checked
description: "Define Helm chart repositories as HTTP/S or OCI sources, with credentials, intervals and the OCI maintenance-mode caveat."
sources:
  - https://fluxcd.io/flux/components/source/helmrepositories/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A HelmRepository is the source of charts for HelmCharts and HelmReleases.

`.spec.type` is `default` (HTTP/S Helm repository with an index) or `oci`. The `oci` type is in maintenance mode; for improved OCI chart support use the OCIRepository API instead.

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata:
  name: podinfo
  namespace: default
spec:
  interval: 5m0s
  url: https://stefanprodan.github.io/podinfo
```

For an OCI repository: `type: oci` with `url: oci://ghcr.io/org/charts`.

`.spec.interval` is how often the index is fetched; when not set it defaults to `1m`, and it has no effect for OCI repositories because there is no index to poll. A spec change is applied immediately. The controller can add jitter so many repositories with equal intervals spread their load.

`.spec.secretRef.name` names a Secret in the same namespace with `username` and `password` for basic auth (TLS client certs go through `certSecretRef`).

`.spec.passCredentials: true` sends those credentials to hosts that differ from the URL host, needed when the index advertises chart URLs on another host. It only applies to HTTP/S repositories and risks credential theft in a man-in-the-middle attack, so enable it only when required.

`.spec.provider` (generic by default; aws, azure or gcp) is for OCI repositories only, as is `insecure: true`, which allows non-TLS HTTP connections.

## Checked

2026-11-08: read the source-controller HelmRepository spec (docs/spec/v1/helmrepositories.md in the fluxcd/source-controller repo, the source of the fluxcd.io page) in part: the intro, type, provider, insecure, interval, url, timeout, secret reference, cert secret and passCredentials sections, via search plus targeted reads. Confirmed: the type values and the OCI maintenance-mode note pointing to OCIRepository, the interval default and its OCI exclusion, immediate handling of spec changes, jitter, basic-auth Secret keys, passCredentials and its risk, and provider and insecure being OCI-only. Removed: the Helm cache memory advice and the flux CLI command, which are not in the spec, and the HelmRelease chartRef detail.

Method: documentation only; no commands were run.
