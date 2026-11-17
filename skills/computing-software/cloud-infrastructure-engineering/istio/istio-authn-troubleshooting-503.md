---
id: computing-software.cloud-infrastructure-engineering.istio.istio-authn-troubleshooting-503
name: istio-authn-troubleshooting-503
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istio-503-troubleshooting, response-flags, uh-nr]
level: practitioner
status: docs-checked
description: "Triage Istio 503s by reading Envoy response flags, checking DestinationRule mTLS and subsets, and port naming."
sources: ["https://istio.io/latest/docs/ops/common-problems/network-issues/", "https://istio.io/latest/docs/ops/configuration/traffic-management/protocol-selection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start with the access log response flag, then the config.

```sh
kubectl logs deploy/web -c istio-proxy | grep ' 503 '
istioctl x describe pod <pod>
istioctl analyze -n shop
```

Common response flags (Istio troubleshooting page): `NR` no route configured, check your DestinationRule or VirtualService; `UO` upstream overflow from circuit breaking, check the circuit breaker configuration in the DestinationRule; `UF` failed to connect to upstream, check for a mutual TLS configuration conflict. In the default log format the flag follows the response code; a custom format must include `%RESPONSE_FLAGS%`.

Common cause of 503 right after applying a DestinationRule: the rule lacks `trafficPolicy.tls.mode: ISTIO_MUTUAL` while mutual TLS is required, so the mode defaults to `DISABLE` and the client sidecar sends plain HTTP to a server that expects TLS. The page says you should only see this if automatic mutual TLS was disabled at install. Keep the DestinationRule TLS mode consistent with the server configuration.

Port naming also matters for L7 behaviour: name a Service port `<protocol>[-<suffix>]` or set `appProtocol`, and `appProtocol` takes precedence if both are set.

Verify: after correcting the cause, the same request returns 200.

## Checked

2026-11-03. Confirmed in the Istio traffic-management problems page (flags `NR`, `UO`, `UF`, `%RESPONSE_FLAGS%`, the DestinationRule `ISTIO_MUTUAL` 503 case and its automatic-mTLS condition) and the protocol selection page (port name or `appProtocol`, precedence). Removed: the `UH` and `URX` flag meanings, the empty-subset cause, the circuit-breaker-too-low and two-sidecar advice, and the `proxy-config cluster` verify step (not on the pages read).

Method: documentation only; no commands were run.
