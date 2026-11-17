---
id: computing-software.devops-ci-cd.argo-rollouts.canary-header-routes-and-mirroring
name: canary-header-routes-and-mirroring
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [canary, setheaderroute, setmirrorroute, managedroutes, header-routing, traffic-mirroring, argo-rollouts]
level: sme
status: docs-checked
description: "Use setHeaderRoute and setMirrorRoute steps, declared in managedRoutes, to target or shadow canary traffic."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two canary steps let a traffic router send selected requests to the canary. Both require `trafficRouting` and a matching entry under `managedRoutes`, which lists the routes Argo Rollouts may manage and whose order sets precedence above routes already in the router.

```yaml
trafficRouting:
  managedRoutes:
    - name: set-header
    - name: mirror-route
steps:
  - setHeaderRoute:
      name: set-header
      match:
        - headerName: version
          headerValue:
            exact: '2'
  - setMirrorRoute:
      name: mirror-route
      percentage: 100
      match:
        - method:
            exact: GET
          path:
            prefix: /
  - setHeaderRoute:
      name: set-header      # no match: removes the route
```

`setHeaderRoute` sends all traffic with the matching header to the canary. `headerValue` takes exactly one of `exact`, `regex` or `prefix`. Per the spec comments, it is supported for Istio and, via the plugin, Gateway API providers.

`setMirrorRoute` mirrors the configured percentage of matched traffic to the canary. Conditions inside a match block are ANDed; the list of match blocks is ORed. It is supported only for Istio at the moment. Not every router supports every match type.

A step without `match` acts as removal of the route. Routes listed in `managedRoutes` are removed at the end of a rollout or on abort, so never list manually created routes there.

Verify by sending a request with the header and checking which pods log it.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/specification/, https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/.

Removed or corrected: the Apache APISIX and AWS ALB support claim and the clean-up-before-final-step advice.

Method: documentation only; no commands were run.
