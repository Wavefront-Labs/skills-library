---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-header-modifier-filters
name: httproute-header-modifier-filters
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, filters, requestheadermodifier, responseheadermodifier, headers, add-set-remove]
level: practitioner
status: docs-checked
description: "Modify request and response headers with HTTPRoute RequestHeaderModifier and ResponseHeaderModifier filters: add, set and remove actions."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-header-modifier.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/httproute.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two filter types, which can be used together on the same HTTPRoute:

- `RequestHeaderModifier`: modifies headers on the request sent to the backend.
- `ResponseHeaderModifier`: modifies headers on the response returned to the client. Extended feature `HTTPRouteResponseHeaderModification`.

The guide marks its request header modifier section with extended feature `HTTPRouteBackendRequestHeaderModification`.

Actions:

- `add`: add a header with the given name and value.
- `set`: unconditionally overwrite the value if the header exists, or create it.
- `remove`: list of header names to delete.

```yaml
filters:
- type: RequestHeaderModifier
  requestHeaderModifier:
    set:
    - name: my-header-name
      value: my-new-header-value
```

```yaml
filters:
- type: RequestHeaderModifier
  requestHeaderModifier:
    remove: ["x-request-id"]
```

```yaml
filters:
- type: ResponseHeaderModifier
  responseHeaderModifier:
    add:
    - name: X-Header-Add-1
      value: header-add-1
    - name: X-Header-Add-2
      value: header-add-2
```

Uses for the response filter: add or remove cookies for one backend, or tell a frontend whether it is talking to a stable or beta backend.

Remember that the order of multiple behaviours across filters is currently unspecified, and specifying one core filter type multiple times has unspecified or implementation-specific behaviour.

## Checked

2026-11-08. Read in full: the HTTP header modifier guide and the HTTPRoute reference page (raw markdown on GitHub; the HTTPRoute page added to sources). Confirmed: the RequestHeaderModifier and ResponseHeaderModifier filter types, add, set and remove actions with the example snippets, the extended feature names HTTPRouteBackendRequestHeaderModification and HTTPRouteResponseHeaderModification, the response-filter use cases, and the unspecified ordering of multiple behaviours and repeated core filters. Reworded: the backendRef-level and append claims, which the pages do not state.

Method: documentation only; no commands were run.
