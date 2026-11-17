---
id: computing-software.cloud-infrastructure-engineering.gateway-api.hostname-precedence-sni-host-and-dns
name: hostname-precedence-sni-host-and-dns
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [hostnames, precedence, sni, host-header, dns, cert-manager]
level: advanced
status: docs-checked
description: "Hostname precedence order, how SNI differs from the HTTP Host header, and what DNS and certificate automation may derive from Routes."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/hostnames.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/traffic-matching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Choosing a Listener: when listeners share port and protocol but differ in hostname, traffic goes to the most specific one, using the intersected hostname (the overlap of listener and Route hostnames). More labels without a wildcard means more specific: `www.example.com` beats `*.example.com`, which beats `*.com`, which beats `*`. The general order is exact match, then most specific wildcard, then general wildcard (including "no hostname", equivalent to `*`).

Choosing a Route when several attach to the same Listener and yield identical intersected hostnames (extended feature `GatewayRouteHostnameIntersectionPrecedence`): the Gateway SHOULD compare the Routes' original `spec.hostnames`, not the intersection. Example: Listener `*.foo.com`, Route A `*.foo.com`, Route B `*.com`; a request to `bar.foo.com` goes to Route A. If original hostnames are equally specific, fall back to the oldest creation timestamp, then alphabetical name order.

SNI versus Host:

- For TLS protocols the intersected hostname must match the request SNI (RFC-2818 rules, so a wildcard certificate name matches a single label) and, with `tls.mode: Terminate`, should be present in the certificate CN or SAN. Gateway API does not require implementations to verify that.
- For HTTPRoute and GRPCRoute the Host (or `:authority`) header must also match the intersected hostname; for Host matching `*` can match more than one label.
- TLSRoute with Passthrough uses SNI only.
- IP addresses are never valid hostnames in Gateway API.

DNS and certificates for integrators:

- Always use the intersected hostname, not the Listener or Route hostname alone. If none can be determined, ignore that Listener and its Routes.
- All intersected hostnames on a Gateway's listeners MUST resolve to all addresses in `status.addresses` (CNAMEs are fine when the address is a hostname).
- Certificates: every intersected hostname must be represented in a generated certificate; do not programmatically generate wildcard certificates from hostname fields.
- Only consider Gateways and Routes with `Accepted` true, and follow the full ownership tree from GatewayClass.

Traffic that fails a listener's routes cannot fall back to another listener (see the traffic matching page).

## Checked

2026-11-08. Read in full (GitHub markdown): the Hostnames page and the Traffic Matching page. Confirmed: listener ordering, route precedence, SNI and Host rules, integrator rules for DNS and certificates. Removed: the claim that a client can send mismatched SNI and Host with implementations deciding enforcement, the "multi-team design tip", and the loose cert-manager framing (not stated as such; the page only names the cert-manager Certificate API for wildcard management).

Method: documentation only; no commands were run.
