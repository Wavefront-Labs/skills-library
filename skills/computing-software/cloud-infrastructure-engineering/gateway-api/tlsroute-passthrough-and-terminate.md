---
id: computing-software.cloud-infrastructure-engineering.gateway-api.tlsroute-passthrough-and-terminate
name: tlsroute-passthrough-and-terminate
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [tlsroute, passthrough, sni, tls, l4, terminate]
level: practitioner
status: docs-checked
description: "Route TLS by SNI with TLSRoute: Passthrough keeps traffic encrypted to the backend, Terminate decrypts at the Gateway; listener protocol TLS and hostnames matter."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/tlsroute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/tls-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`TLSRoute` routes TLS connections using the server name (SNI) from the ClientHello.

Listener side: use a listener with `protocol: TLS`, and set `tls.mode`:

- `Passthrough`: the Gateway does not decrypt. It reads SNI, picks the Route by hostname, and forwards the encrypted stream to the backend, which must hold the certificate.
- `Terminate`: the Gateway terminates TLS using the certificate configured on the listener, then forwards the unencrypted TCP stream to the backend.

Route side: `parentRefs` attach the TLSRoute to the Gateway (optionally with `sectionName` or `port`), `hostnames` (required, unlike HTTPRoute and GRPCRoute) are matched against the SNI hostname, and `rules[].backendRefs` list at least one backend. The listener `tls.mode` field is mandatory for TLS listeners.

Use TLSRoute when:

- The backend must see the original TLS session (end-to-end encryption, including mutual TLS with client certificates).
- The backend is TLS-based but not HTTP-based, for example Kafka or Postgres with a TLS listener.

Use HTTPRoute instead when HTTP/L7 matching is enough; TLSRoute is for the cases where direct encrypted communication to the backend is required.

Release channel and features: the TLSRoute reference says it is GA and in the Standard Channel since v1.5.0. Implementations report the features `TLSRoute` (Passthrough mode, mandatory for any implementation claiming TLSRoute), `TLSRouteModeTerminate` and `TLSRouteModeMixed` (two TLS listeners with distinct modes on the same port).

For hostname intersection with listeners and wildcard behaviour, see the Hostnames concept document.

## Checked

2026-11-08. Read in full: the TLSRoute reference and the TLS routing guide (raw markdown on GitHub). Confirmed: SNI-based routing, Passthrough versus Terminate behaviour, mandatory tls.mode on TLS listeners, required hostnames, at least one backendRef, sectionName and port attachment, the TLSRoute, TLSRouteModeTerminate and TLSRouteModeMixed features, and Standard Channel since v1.5.0. Replaced: the earlier note that channel status was inconsistent across pages. Removed: per-connection weight splitting and the claim that hostnames follow the same wildcard rules as other Routes (point to the Hostnames concept document instead).

Method: documentation only; no commands were run.
