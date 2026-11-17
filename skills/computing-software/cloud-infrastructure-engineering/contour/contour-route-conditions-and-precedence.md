---
id: computing-software.cloud-infrastructure-engineering.contour.contour-route-conditions-and-precedence
name: contour-route-conditions-and-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [request-routing, conditions, prefix, exact, regex, header-conditions, queryparameter, method-matching, precedence]
level: practitioner
status: docs-checked
description: "HTTPProxy route conditions: prefix, exact, regex, header and queryParameter operators, matching HTTP method via :method, and specificity-based route ordering."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/request-routing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy route conditions and precedence

An HTTPProxy needs at least one route or include. Each route has `conditions` combined with AND. A condition block holds at most one of `prefix`, `exact`, `regex` (all must start with `/`); `exact` and `regex` are not allowed in include conditions.

```yaml
routes:
- conditions: [{prefix: /blog}]        # /blog and /blog/*
  services: [{name: s2, port: 80}]
- conditions: [{exact: /feed}]
  services: [{name: s2, port: 80}]
- conditions:
  - header: {name: ":method", exact: GET}
  - queryParameter: {name: os, exact: other, ignoreCase: true}
  services: [{name: s3, port: 80}]
```

Header condition: required `name`, one operator among `present`, `notpresent`, `contains`, `notcontains`, `exact`, `notexact`, `regex`; modifiers `ignoreCase` (not for regex) and `treatMissingAsEmpty` (only for negative matches, default false).

Method matching has no dedicated field; match the `:method` pseudo-header with `exact: GET`.

Query parameter condition: `name` (case-sensitive) plus `exact`, `prefix`, `suffix`, `regex`, `contains` or `present`; `ignoreCase` applies to the value for all but `regex` and `present`.

Precedence: Contour sorts routes by specificity before sending to Envoy, so spec order does not matter. Order: exact paths, then regex (longer first), then prefix (longer first); ties broken by more header conditions, then more query parameter conditions. This mirrors Gateway API HTTPRouteRule precedence.

## Checked

2026-11-08. Read the Contour main-branch config page request-routing.md in full. Confirmed: at least one route or include, AND-combined conditions, one of prefix, exact or regex per block, the leading `/` rule, exact and regex not allowed in include conditions, header operators and modifiers, `:method` header matching, query parameter operators and case-sensitive names, and the specificity sort order. No claims removed.

Method: documentation only; no commands were run.
