---
id: computing-software.devops-ci-cd.argo-rollouts.web-metric-provider
name: web-metric-provider
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [web, http, jsonpath, metric-provider, webhook, analysis, argo-rollouts]
level: practitioner
status: docs-checked
description: "Call an HTTP endpoint as an analysis metric, extract values with jsonPath and send GET, POST or PUT requests."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/analysis/web/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The web provider performs an HTTP request and feeds the response into `result`. The response must return JSON. The optional `jsonPath` expression selects part of it into `result`; without `jsonPath` the entire body is `result`.

```yaml
metrics:
  - name: webmetric
    successCondition: "result.ok && result.successPercent >= 0.90"
    provider:
      web:
        url: "http://my-server.com/api/v1/measurement?service={{ args.service-name }}"
        timeoutSeconds: 20     # default 10
        headers:
          - key: Authorization
            value: "Bearer {{ args.api-token }}"
        jsonPath: "{$.data}"
```

If the result is a string, `asInt` and `asFloat` convert it so numeric comparisons work.

Methods: `method` is GET (default), POST or PUT. Use `body` for raw strings or `jsonBody` for JSON (Content-Type is set automatically). A body on a GET request is an error, and setting both `body` and `jsonBody` is an error.

`insecure: true` skips TLS verification.

OAuth2: under `authentication.oauth2` set `tokenUrl`, `clientId`, `clientSecret` (from a secret arg) and `scopes`; the run gets a token and sends it as an `Authorization: Bearer` header, so you do not add that header yourself.

Verify by hitting the URL with curl and comparing with the AnalysisRun's recorded measurement.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/analysis/web/.

Removed or corrected: plain-text body support and the empty-body behaviour (the page says the response must be JSON).

Method: documentation only; no commands were run.
