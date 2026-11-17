---
id: computing-software.cloud-infrastructure-engineering.observability.load-balancing-otlp-grpc-to-collector-gateways
name: load-balancing-otlp-grpc-to-collector-gateways
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [gateway-load-balancer, otlp-grpc-load-balancing, collector-deployment, otel-collector, grpc]
level: advanced
status: docs-checked
description: "Spread OTLP gRPC across collector gateway replicas: why L4 balancers pin clients, L7 balancers, gRPC balancer_name, sidecars, and when to use the loadbalancing exporter."
sources: ["https://opentelemetry.io/docs/collector/scaling/", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configgrpc/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load balancing OTLP gRPC to gateways

## The problem (Collector scaling guide)
When gRPC receives the data, as is common with OTLP, use a load balancer that understands gRPC (L7). A standard
L4 load balancer may establish a persistent connection to a single backend Collector, negating the benefits of
scaling, because clients keep hitting the same Collector.

## Options the docs support
- **L7 balancing**: in Kubernetes, prefer off-the-shelf solutions such as service meshes (Istio, Linkerd) or cloud
  provider load balancers, which also add traffic management and resilience features.
- **Sidecars**: when node count is low and pod count high, a sidecar Collector gives better gRPC balancing among
  Collector layers without a gRPC-specific balancer, and avoids one failed DaemonSet pod taking out a whole node's
  telemetry. The Operator injects one when the Collector CR has `mode: sidecar` and the pod has annotation
  `sidecar.opentelemetry.io/inject: 'true'`.
- **Client-side balancer**: the OTLP gRPC client settings include `balancer_name`. The default was `pick_first`
  before Collector v0.103.0 and is `round_robin` from v0.103.0; set `balancer_name: pick_first` to restore the old
  behaviour.
- **Server keepalive**: the gRPC receiver settings expose `keepalive.server_parameters` (`max_connection_age`,
  `max_connection_age_grace`, `max_connection_idle`) and an `enforcement_policy` (`min_time`,
  `permit_without_stream`). The config README lists them without describing balancing effects, so test before
  relying on them to rebalance.

## The loadbalancing exporter is for affinity
Use it in front of stateful components (tail sampling, span-to-metrics): it hashes trace ID or service name
consistently and can take hosts from a DNS A record (such as a Kubernetes headless service) or a static list.
Do not treat it as a generic even spread. Lower its resolver interval in highly elastic environments, since
Collectors may resolve DNS at different times.

## Verify
- [ ] Per-pod receiver traffic (for example `otelcol_receiver_accepted_spans`) is roughly even a few minutes after
  scaling out.

## Checked
2026-11-09. Confirmed against the opentelemetry.io Collector scaling page (read as raw markdown) and the
configgrpc README (searched for balancer_name and keepalive settings). Removed unconfirmed claims and sources:
ClusterIP connection-level behaviour, the headless-Service `dns:///` round_robin recipe, the claim that
`max_connection_age` makes clients land on other pods, ingress annotations, AWS ALB gRPC advice, OTLP/HTTP
comparison and the 20% evenness threshold, plus the Kubernetes blog source (not read).
Method: docs-checked 2026-11-09 against the Collector scaling page markdown and the configgrpc README; documentation only, no commands run.
