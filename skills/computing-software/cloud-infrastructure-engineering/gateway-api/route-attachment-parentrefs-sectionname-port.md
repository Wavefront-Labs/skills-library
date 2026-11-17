---
id: computing-software.cloud-infrastructure-engineering.gateway-api.route-attachment-parentrefs-sectionname-port
name: route-attachment-parentrefs-sectionname-port
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [parentrefs, sectionname, port, route-attachment, listener]
level: practitioner
status: docs-checked
description: "Attach Routes to Gateways with parentRefs: namespace, sectionName and port selectors, the AND rule, and the trade-off of binding by port number."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/httproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/tcp.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/traffic-matching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Route must have a `parentRefs` entry referencing a Gateway (or one of its listeners via `sectionName`) to be a compliant Route. Attachment requires two things: the Route references the Gateway, and at least one Listener on the Gateway allows the attachment (via `allowedRoutes` kinds and namespaces, and hostname intersection).

```yaml
spec:
  parentRefs:
  - name: acme-lb              # namespace optional if same namespace
    sectionName: foo           # select listener by name
```

Selectors in a `parentRef`:

- `sectionName`: selects the listener with that `name`. If no listener has that name, the set of relevant listeners is empty and the parentRef is ignored.
- `port`: selects all listeners listening on that port with a protocol compatible with the Route kind. This is an Extended feature (`HTTPRouteParentRefPort`); implementations list support in `GatewayClass` `status.supportedFeatures`.
- Both set: the listener must satisfy both (name AND port).
- Neither set: by default the Route attaches to all listeners of the Gateway.

Binding by `port` couples the Route to the Gateway: admins can no longer switch ports on the Gateway without updating the Routes. Use it only when the Route should apply to that specific port number; binding to port 8090 is convenient when two listeners (`bar`, `baz`) share it.

TCP example: `sectionName: foo` pointing at listener `name: foo` (TCP, port 8080) gives the same result as `port: 8080`. A TCPRoute can attach only to a TCP listener; attaching it to an HTTP or HTTPS listener leaves the route not accepted. A Route may also list several parentRefs, to different sections of one Gateway or to different Gateways (many-to-one).

Successful attachments are counted in the listener's `status.attachedRoutes`; the Route's `status.parents` lists one entry per parent.

## Checked

2026-11-08. Read in full (GitHub markdown): the API overview, HTTPRoute reference, TCP routing guide and traffic matching page. Confirmed: parentRefs requirement, sectionName and port semantics and the AND rule, default of all listeners, port-binding trade-off, Extended feature name, TCP listener restriction, attachedRoutes and status.parents. Removed: nothing unconfirmed remained other than the unsupported "compatible listeners" wording for the no-selector case.

Method: documentation only; no commands were run.
