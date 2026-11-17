---
id: computing-software.cloud-infrastructure-engineering.gateway-api.route-merging-and-conflict-resolution
name: route-merging-and-conflict-resolution
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [conflicts, merging, precedence, creationtimestamp, route-merging, api-design]
level: advanced
status: docs-checked
description: "How Gateway API resolves conflicts and merges Routes: keep working config, most specific match first, oldest creation timestamp, then namespace/name."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/api-design/_index.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/httproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/getting-started/migrating-from-ingress.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/hostnames.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Because roles are separated, two teams may submit configuration for the same path. Where a field documents its own resolution, follow that; otherwise these principles apply (API Design Guide):

- Prefer not to break things that are working.
- Drop as little traffic as possible.
- Provide a consistent experience and make it clear which path was chosen, by setting status conditions on the relevant resources where possible.
- More specific matches take precedence over less specific ones.
- The resource with the **oldest creation timestamp** wins.
- If still equivalent, the first alphabetically by `namespace/name` wins (`foo/bar` beats `foo/baz`).

Merging: multiple HTTPRoutes can attach to one Gateway (GRPCRoute follows the same merging semantics), but **only one Route rule may match each request**. Ingress APIs do not prescribe merging or conflict resolution, so Ingress controllers differ; Gateway API prescribes it: an implementation must merge the routing rules from all HTTPRoutes attached to a listener and handle conflicts per the API Design Guide, for example more specific matches win over less specific ones.

Hostnames: when several Routes attach to one Listener and yield identical intersected hostnames, the Gateway SHOULD compare the Routes' original `spec.hostnames` by specificity first (a Route with `*.foo.com` beats one with `*.com` on a `*.foo.com` listener); creation timestamp (oldest wins) is used only to break a tie, then alphabetical name. This is the extended feature `GatewayRouteHostnameIntersectionPrecedence`.

Single-resource consistency: the Kubernetes API only guarantees consistency per resource, so cross-resource error checking is asynchronous and eventually consistent, and controllers must handle broken links between resources.

## Checked

2026-11-08. Read in full (GitHub markdown): the API Design Guide, HTTPRoute reference, Migrating from Ingress guide and Hostnames page. Confirmed: conflict principles in order, merging requirement and the one-rule-per-request statement, hostname precedence and its feature name, single-resource consistency. Removed: the TCPRoute/UDPRoute "all Accepted but only the oldest receives traffic" claim, the ListenerSet conflict claim, and the "flat rule list" wording, none of which appear in the cited pages. Added the Hostnames page as a source.

Method: documentation only; no commands were run.
