---
id: computing-software.cloud-infrastructure-engineering.gateway-api.running-conformance-tests
name: running-conformance-tests
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [conformance, tests, go-test, supported-features, gateway-class, make]
level: advanced
status: docs-checked
description: "Run the conformance suite against a Gateway API implementation: key flags, namespace labels and annotations, cleanup, single-test runs, and building the test binary."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/conformance/running-tests.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/conformance/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The suite lives in the Gateway API repository and runs with `go test`.

```
go test ./conformance -run TestConformance -args --gateway-class=my-class
```

Useful flags from the running-tests page:

- `--gateway-class`: the GatewayClass to test. Without it the suite expects a class named `gateway-conformance`.
- `--supported-features`: by default the suite infers features from GatewayClass status; when this flag is set, only the listed features are enabled (for example `Gateway,HTTPRoute,ReferenceGrant`, or `Mesh` for mesh tests).
- `--exempt-features`: removes features from a manual selection.
- `--namespace-labels` and `--namespace-annotations`: name=value labels or annotations set on the test namespaces (for example `linkerd.io/inject=enabled`).
- `--cleanup-base-resources=false`: skip cleanup of test resources so you can inspect the cluster after a failure.
- `--run-test`: run one test by name.

If the CNI enforces network policies, you must add the NetworkPolicy resources some tests need.

Build a standalone binary with `make conformance-bin` (output `conformance.test`, run as `./conformance.test <flags>`) to run on a different environment; pass `GOOS` and `GOARCH` to `make` for other architectures.

## Checked

2026-11-04. Confirmed on the Gateway API conformance running-tests page (running-tests.md): go test command, flags and defaults above, network policy note, make target. Removed the generic process list, the BackendTLSPolicy union remark and the `--help` tip (not on the page). Fixed `--cleanup-base-resources`, which skips cleanup when false rather than removing resources.

Method: documentation only; no commands were run.
