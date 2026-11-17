---
id: computing-software.devops-ci-cd.flagger.flagger-ab-testing-match
name: flagger-ab-testing-match
category: computing-software
field: devops-ci-cd
product: flagger
tags: [ab-testing, match, headers, cookies, iterations]
level: advanced
status: docs-checked
description: "Configure Flagger A/B testing with HTTP header and cookie match conditions and iterations, with provider-specific matching limits."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use A/B testing for apps needing session affinity: users matching a header or cookie stay on the same version for the whole analysis. If a `match` is present, Flagger ignores `maxWeight` and `stepWeight`.

```yaml
analysis:
  interval: 1m
  iterations: 10
  threshold: 2
  match:
    - headers:
        x-canary:
          regex: ".*insider.*"
    - headers:
        cookie:
          regex: "^(.*?;)?(canary=always)(;.*)?$"
```

Header keys must be lowercase with hyphens. Value matchers: `exact`, `prefix`, `suffix`, `regex` (RE2). Minimum run time is `interval * iterations`; rollback time `interval * threshold`.

Provider limits: Istio also supports `sourceLabels` (only if the `mesh` gateway is in `service.gateways`); App Mesh supports a single condition; Contour has no regex (prefix, suffix, exact); NGINX supports only exact cookie names whose value must be `always`, with regex header matching since ingress v0.31. Test with `curl -H 'X-Canary: insider' http://app.example.com` or `curl -b 'canary=always' ...`.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/deployment-strategies.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
