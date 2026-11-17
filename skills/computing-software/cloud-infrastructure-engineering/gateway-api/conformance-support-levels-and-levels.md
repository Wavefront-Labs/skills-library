---
id: computing-software.cloud-infrastructure-engineering.gateway-api.conformance-support-levels-and-levels
name: conformance-support-levels-and-levels
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [conformance, core, extended, implementation-specific, partial, conformant]
level: advanced
status: docs-checked
description: "Read Gateway API conformance: Core, Extended and implementation-specific support levels, Conformant versus Partial, and Partial's deprecation."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/conformance/_index.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/conformance/levels.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Conformance tells users what an implementation does consistently.

**Support levels of a feature**

- Core: portable, with a reasonable roadmap expected for ALL implementations towards support.
- Extended: portable but not universally supported; implementations that support the feature have the same behaviour and semantics. Some may migrate into Core. Extended features are part of the API types and schema.
- Implementation-specific: not portable and vendor-specific; no API types or schema except via generic extension points, and not covered by conformance tests.

Core and Extended behaviour is validated by behaviour-driven conformance tests. Where support levels overlap for a field, the minimum level applies: HTTPRoute filters are Core within a Rule but Extended within a BackendRef, so a Core field in a filter inside a BackendRef is interpreted as Extended.

**Implementation levels** from the levels page:

Levels come from conformance reports submitted to the Gateway API repo.

- Conformant: the report is from a publicly available, tagged version (prereleases such as `v1.2.3-pre.0` are fine, commit hashes are not); all profiles pass with no skipped tests; at least one report is Conformant if several are submitted; and it is for the latest Gateway API release `n` or `n-1`. An implementation must support at least one profile and one Route type in it, passing all Core tests for them plus every Extended feature it claims.
- Partial: a profile reports a `partial` result (for example skipped tests), and/or the supported Gateway API version is exactly `n-2`. Such an implementation can only be Partially Conformant.
- The Partial state is deprecated and will be removed entirely in the v1.8 release.

Traffic types: Gateway controllers reconcile Gateway resources for north-south traffic; Mesh controllers reconcile Services with HTTPRoutes attached for east-west traffic. An implementation may handle both, and each has its own conformance tests.

Where to look:

- Implementations run the conformance suite and submit the report by PR to the reports folder in the Gateway API repo; tooling then updates the implementations list and feature matrices automatically. Currently tests cover the majority of Standard channel capabilities, Core and Extended.
- Prerelease reports are stored separately, are not used for the implementations list, feature matrices or feature wizard, may use a commit hash, and may run only the tests for the feature being proven.

Reading a report (derived from the rules above): check the Gateway API version against the current release, which profiles passed, and whether the Extended features you need are claimed.

Do not assume a feature works because the CRD field exists: the CRD is the API, conformance is evidence that a controller implements it.

## Checked

2026-11-08. Read in full: the Conformance overview and Levels pages (raw markdown on GitHub). Confirmed: Core, Extended and implementation-specific definitions, minimum-level rule for overlapping support (HTTPRoute filter example), Conformant and Partial criteria including n, n-1 and n-2 versions, deprecation and removal of Partial in v1.8, Gateway versus Mesh traffic types, report submission by PR, and prerelease report handling. Removed: the status.supportedFeatures pointer, the example feature name, the claim that reports are tagged by channel, and the earlier simplified definition of Partial. The final reading checklist is derived, not quoted.

Method: documentation only; no commands were run.
