---
id: computing-software.cloud-infrastructure-engineering.gateway-api.listenerset-attach-and-configure
name: listenerset-attach-and-configure
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [listenerset, listeners, allowedlisteners, delegation, multi-tenant]
level: advanced
status: docs-checked
description: "Delegate listener management with ListenerSet: attach extra listeners to a Gateway, control it with allowedListeners None, Same, All or Selector, and the 64-listener limit."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/listenerset.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/listener-set.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `ListenerSet` lets teams define listeners (with their own hostnames, ports and certificates) outside the Gateway object, so the Gateway owner does not have to edit one large resource. It works around the 64-listener limit per Gateway and supports self-service TLS for tenants.

Attachment is two-sided:

- The ListenerSet has a `parentRef` to the Gateway.
- The Gateway opts in with `spec.allowedListeners.namespaces.from`: `None` (default, no ListenerSets), `Same`, `All`, or `Selector`.

Routes then attach to a ListenerSet listener with a `parentRef` whose `kind` is `ListenerSet`.

With `Selector` you must also provide the `selector` field. A Route with no `sectionName` attaches to all listeners in the ListenerSet.

ListenerSet is Standard channel since v1.5.0.

Status: the Gateway reports the number of attached ListenerSets in `status.attachedListenerSets`. Each ListenerSet has top-level `Accepted` and `Programmed` conditions, and each listener its own status entry. See the ListenerSet conflicts skill for how clashes between listeners are resolved.

## Checked

2026-11-04. Confirmed on the Gateway API ListenerSet reference (listenerset.md): Standard channel since v1.5.0, allowedListeners values and default, parentRef, route attachment, 64-listener limit, attachedListenerSets, conditions. Removed the "newer API, confirm availability" tip and the allowedRoutes-constraints sentence (not on the page); removed the experimental tag.

Method: documentation only; no commands were run.
