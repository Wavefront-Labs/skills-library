---
id: computing-software.cloud-infrastructure-engineering.istio.istio-istioctl-analyze
name: istio-istioctl-analyze
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istioctl-analyze, config-validation, ist0102]
level: practitioner
status: docs-checked
description: "Run istioctl analyze on a live cluster or local YAML to catch missing injection, bad references and conflicts, and suppress accepted messages."
sources: ["https://istio.io/latest/docs/ops/diagnostic-tools/istioctl-analyze/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`istioctl analyze` is read-only: it never changes configuration state. It can run against a live cluster, local files, or both (files simulated on top of the cluster).

```sh
istioctl analyze --all-namespaces
istioctl analyze --namespace default
istioctl analyze samples/bookinfo/networking/*.yaml              # live cluster plus these files
istioctl analyze --use-kube=false samples/bookinfo/networking/*.yaml  # files only
istioctl analyze -k --namespace frod --suppress "IST0102=Namespace frod"
```

Messages carry a level and code, for example `Info [IST0102]` (namespace not enabled for injection), `Error [IST0101]` (referenced selector or host not found) and `Warning [IST0174]` (DestinationRule host matches no service). Message details and fixes are in the configuration analysis messages reference.

Suppression: `--suppress "<code>=<kind> <name>.<namespace>"` (just `<kind> <name>` for cluster-scoped resources like Namespace); repeat the flag or use wildcards, for example `--suppress "IST0107=Pod *.baz"`. Or annotate the resource: `kubectl annotate deployment my-deployment galley.istio.io/analyze-suppress=IST0107` (comma-separate several codes).

Gotchas: with `--use-kube=false` the file set is expected to be fully self-contained, otherwise you get reference-not-found messages. Analysis is generally backwards compatible, so a newer istioctl can analyze an older cluster; keep that binary in a separate folder from the one managing your deployed release. An experimental `istiod.enableAnalysis` setting (`istioctl install --set values.global.istiod.enableAnalysis=true`) writes the same messages into resource `status.validationMessages`; it is not a replacement for `istioctl analyze`.

## Checked

2026-11-03. Confirmed against the Istio istioctl analyze page: all commands, message codes and levels, suppression syntax and annotation, backwards-compatibility note, `enableAnalysis`. Removed: the CI-gate exit-code claim and rule curation advice, the invented VirtualService verify step, and the `-n shop file.yaml` example.
Method: documentation only; no commands were run.
