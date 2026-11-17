---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-filters-compatibility-and-support-levels
name: httproute-filters-compatibility-and-support-levels
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, filters, core, extended, implementation-specific, incompatiblefilters, extensionref]
level: advanced
status: docs-checked
description: "Understand HTTPRoute filter support levels (Core, Extended, implementation-specific), which filters cannot combine, and the IncompatibleFilters reason."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/httproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/conformance/_index.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Filters are an extension point for request/response processing: modification, authentication, rate limiting, traffic shaping.

Conformance by filter type:

- Core filters MUST be supported by implementations.
- Extended filters: implementers are encouraged to support them.
- Implementation-specific filters have no API guarantees across implementations.

Rules and caveats:

- All filters are expected to be compatible **except** `URLRewrite` and `RequestRedirect`, which may not be combined.
- If an implementation cannot support other combinations it must document that. When an incompatible or unsupported filter set makes `Accepted` go `False`, it may use reason `IncompatibleFilters`.
- Ordering of multiple behaviours is currently unspecified.
- Specifying a core filter multiple times has unspecified or implementation-specific conformance.

Overlapping support levels: the minimum applies. HTTPRoute has Core support for filters in a rule and Extended support for filters inside a `backendRef`; a Core field inside a backendRef filter is interpreted as Extended.

## Checked

2026-11-04. Confirmed on the Gateway API HTTPRoute reference and conformance page (httproute.md, conformance/_index.md): filter purpose, Core/Extended/implementation-specific levels, URLRewrite and RequestRedirect incompatibility, IncompatibleFilters reason, unspecified ordering, minimum-level overlap rule. Removed the extensionRef example, supportedFeatures pointer, feature-name list and the GRPCRoute filter-reuse remark (not on the fetched pages).

Method: documentation only; no commands were run.
