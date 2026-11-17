---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.http-api-authorization-with-bundles
name: http-api-authorization-with-bundles
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [http-api, authorization, bundles, docker-compose, manager-hierarchy]
level: practitioner
status: docs-checked
description: "Authorise HTTP API calls with a Rego policy served as a bundle: own-resource and manager-of rules, path-array matching and the --set flags that wire the bundle service."
sources:
  - https://www.openpolicyagent.org/docs/http-api-authorization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a service ask OPA whether a request is permitted, with policy shipped as a bundle.

Target policy from the tutorial: people can read their own salary (`GET /finance/salary/{user}`), and a manager can read their direct reports' salaries.

```rego
package httpapi.authz

# bob is alice's manager, and betty is charlie's.
subordinates := {"alice": [], "charlie": [], "bob": ["alice"], "betty": ["charlie"]}

default allow := false

allow if {
    input.method == "GET"
    input.path == ["finance", "salary", input.user]
}

allow if {
    some username
    input.method == "GET"
    input.path = ["finance", "salary", username]
    subordinates[input.user][_] == username
}
```

The request path arrives as an array (`["finance", "salary", "alice"]`), so comparing arrays matches both the fixed segments and the user in one expression.

Build and serve:

```
opa build example.rego
```

This writes `bundle.tar.gz`; put it on a bundle server. The tutorial runs OPA in a container with these flags:

```
run --server --addr=0.0.0.0:8181 --log-format=json-pretty
--set=decision_logs.console=true
--set=services.nginx.url=http://bundle_server
--set=bundles.nginx.service=nginx
--set=bundles.nginx.resource=bundles/bundle.tar.gz
```

The tutorial warns that this OPA runs with no authorisation policy, so clients can read and write policies; see the Security page before exposing it.

Check: query as bob for alice's salary (allowed) and as alice for bob's (denied), and watch the console decision log for each.

## Checked

2026-11-04. Confirmed against the OPA docs page HTTP API Authorization (http-api-authorization). Nothing removed.

Method: documentation only; no commands were run.
