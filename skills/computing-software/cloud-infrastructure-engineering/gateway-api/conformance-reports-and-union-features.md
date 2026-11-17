---
id: computing-software.cloud-infrastructure-engineering.gateway-api.conformance-reports-and-union-features
name: conformance-reports-and-union-features
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [conformance, reports, union-features, prerelease, implementers, backendtlspolicy]
level: sme
status: docs-checked
description: "Implementer view of conformance: submitting reports, prerelease reports, supportedFeatures and union features such as BackendTLSPolicy."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/conformance/_index.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/implementers-guide/_index.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/conformance/changelog.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Conformance exists to give publicly available, reproducible reports that users can use to verify claimed support. Implementations run the conformance suite, take the output and submit the report to the Gateway API repo; tooling then updates the conformant-implementation lists and feature matrices. Support levels are Core, Extended and implementation-specific; the last is not covered by conformance tests.

Rules for implementers (Implementer's Guide):

- A conformant implementation passes the suite of the bundle version with no skipped tests (skips are acceptable only during development). Extended features may be disabled. Conformance is version-specific, and the suite output includes the Gateway API version supported.
- Publish supported features in `status.supportedFeatures` of each GatewayClass you accept: entries are objects with a `name`, sorted ascending alphabetically, at most 64 entries, and published before or in the same update as the `Accepted` condition. Only publish Gateway features there (Mesh features go on the experimental XMesh resource), and only publish a feature that passes its tests. Use `--supported-features` only in development or for Mesh features.
- Reconcile GatewayClasses whose `controllerName` matches, set `Accepted` true or false accordingly, and update status only for in-scope Routes and Gateways, setting `observedGeneration` to `metadata.generation`.
- Implementations of Gateway and GatewayClass must set the `SupportedVersion` condition indicating whether the installed CRD version is supported.

Union features: a union feature applies to any other feature sharing a compatible surface. BackendTLSPolicy is the guide's example, along with ReferenceGrant (Core). An implementation that supports a union feature MUST support it in combination with every other reported feature where applicable, for example BackendTLSPolicy with GRPCRoute, with TLSRoute Terminate listeners, or with `requestMirror.backendRef` of type Service. Union features must appear in the ExtendedFeatures set of every applicable conformance profile (BackendTLSPolicy in GATEWAY-HTTP, GATEWAY-GRPC and GATEWAY-TLS). Conformance tests declare required features and run only when all are claimed, so a failing combination test means the combination is not supported; the report output lists supported and unsupported features per profile.

Conformance changelog highlights:

- v1.7: all profiles in a report must be at least partially conformant; an implementation is conformant if one entire report is Conformant; partial conformance is deprecated (at most 5 skipped tests across a report); reports must be reproducible and may only come from released versions usable by the public; prerelease reports were added so features have enough conformant implementations to graduate to Standard.
- v1.6: the Stale category was removed; reports for version n or n-1 can be conformant, n-2 only partially conformant, n-3 or older no longer conformant.
- Proposed for v1.8: partial conformance removed and reports with skipped tests not accepted.

## Checked

2026-11-08. Read in full (GitHub markdown): the Conformance page, the Implementer's Guide and the conformance changelog. Confirmed everything above from those pages. Removed: the claim that a report records channel and implementation version (the guide only says the suite output includes the API version and per-profile feature lists), that reports are filed under the release they cover, the "tolerate broken references" checklist item and the marketing remark (inference).

Method: documentation only; no commands were run.
