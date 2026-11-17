---
id: computing-software.cloud-infrastructure-engineering.gateway-api.listenerset-conflicts-and-status
name: listenerset-conflicts-and-status
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [listenerset, conflicts, status, listener, precedence, accepted]
level: advanced
status: docs-checked
description: "Understand how ListenerSet listeners conflict with the Gateway listeners and each other, which one wins, and how to read the resulting status conditions."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/listenerset.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/listener-set.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ListenerSet is Standard Channel since v1.5.0 per the reference page; the user guide labels it an Extended feature. Listeners are distinct across a group of listeners (one ListenerSet, or the group attached to a Gateway) by the combination of port, protocol and, depending on the protocol, hostname. A conflict arises when listeners claim the same port, protocol and/or hostname.

Priority when two listeners clash:

1. The Gateway's own listeners win over any ListenerSet listener.
2. Between ListenerSets, the one with the older `creationTimestamp` wins.
3. If timestamps are identical, the alphabetically first `{namespace}/{name}` wins.

The winning listener is Accepted and Programmed. The reference page marks the losing listener with `Conflicted: True`; the user guide says the losing ListenerSet gets `Accepted: false` and `Conflicted: true`. Adding a new conflicting ListenerSet never takes over an existing config, which keeps traffic stable. A ListenerSet can be partially accepted: valid listeners keep routing and conflicted ones do not.

Reading status:

- On the Gateway, `.status.attachedListenerSets` reports the number of attached ListenerSets.
- A ListenerSet has top-level `Accepted` and `Programmed` conditions; `Accepted: False` can be set for reasons such as the parent Gateway not allowing ListenerSets or all listeners being invalid. Each listener in the set has its own status entry, following the same logic as Gateway listeners.
- Attachment needs all three: the Gateway's `spec.allowedListeners` selecting the ListenerSet's namespace (`namespaces.from` is `None` by default, or `Same`, `All`, `Selector`), a valid `parentRef` pointing back to the Gateway, and the controller accepting the resource.

Practical rule (derived): give each ListenerSet distinct hostnames and do not reuse a port, protocol and hostname already on the Gateway.

## Checked

2026-11-08. Read in full: the ListenerSet reference page and the ListenerSet user guide (raw markdown on GitHub). The API design guide was dropped from sources and its claim removed. Confirmed: conflict definition and distinctness, the three-level priority order, Conflicted condition, partial acceptance, allowedListeners values and default, the three attachment requirements, attachedListenerSets, and the Accepted and Programmed conditions. The two pages word the losing-side conditions slightly differently and both are given. The practical rule is a derived suggestion.

Method: documentation only; no commands were run.
