---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-method-and-query-param-matching
name: httproute-method-and-query-param-matching
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, method-match, queryparams, header-match, httproutemethodmatching, httproutequeryparammatching]
level: practitioner
status: docs-checked
description: "Match HTTPRoute requests on HTTP method and query parameters, combine them with path and header matches, and OR them across match entries (extended features)."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-method-matching.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-query-param-matching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both are Extended features: `HTTPRouteMethodMatching` and `HTTPRouteQueryParamMatching`.

Method matching:

```yaml
rules:
- matches:
  - method: POST
  backendRefs:
  - name: infra-backend-v1
    port: 8080
- matches:
  - method: GET
  backendRefs:
  - name: infra-backend-v2
    port: 8080
```

Query parameter matching:

```yaml
- matches:
  - queryParams:
    - name: animal
      value: dolphin
    - name: color
      value: blue
```

Rules for combining:

- Fields inside one match are ANDed: `path` + `method`, `headers` + `method`, `path` + `headers` + `method`, `path` + `queryParams`, and so on.
- Multiple params inside one `queryParams` list are ANDed (`animal=dolphin` AND `color=blue`).
- Multiple entries in `matches` are ORed: for example `PATCH /path3` OR (`DELETE /path4` with header `version: three`); or `animal=dolphin&color=blue` OR `ANIMAL=Whale`.

## Checked

2026-11-04. Confirmed on the Gateway API method matching and query parameter matching guides (http-method-matching.md, http-query-param-matching.md): both Extended feature names, method and queryParams examples, AND within a match, OR across matches, combinations with path and headers. Removed the supportedFeatures tip, the case-sensitivity remark and the catch-all advice (not stated on the pages).

Method: documentation only; no commands were run.
