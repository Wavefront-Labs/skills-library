---
id: computing-software.cloud-infrastructure-engineering.aws.elastic-load-balancing
name: elastic-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elb, load-balancer, alb, application-load-balancer, nlb, network-load-balancer, gwlb, gateway-load-balancer, target-group, listener-rules, health-checks, cross-zone-load-balancing, sticky-sessions, deregistration-delay, connection-draining, tls-termination, sni, mtls, access-logs, idle-timeout, http-502, http-504, static-ip, privatelink, geneve, lcu, zonal-shift]
level: practitioner
status: draft
description: "Choose and configure ALB, NLB and Gateway Load Balancer: listeners and rules, target groups and health checks, cross-zone and draining, TLS and mTLS, logs, and the 502/504 failure modes to fix."
sources: ["Elastic Load Balancing User Guide - Application Load Balancers (listeners, rules, target groups)", "Elastic Load Balancing User Guide - Network Load Balancers (TLS listeners, client IP preservation, security groups)", "Elastic Load Balancing User Guide - Gateway Load Balancers (Geneve, endpoints)", "Elastic Load Balancing User Guide - Troubleshoot your Application Load Balancers (HTTP 502, 504)", "Elastic Load Balancing User Guide - Cross-zone load balancing and zonal shift", "Elastic Load Balancing pricing - Load Balancer Capacity Units"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Elastic Load Balancing — ALB, NLB and Gateway Load Balancer, configured for production

**Goal:** the right balancer in front of each workload, targets that drain instead of
dropping connections, health checks that reflect readiness, TLS terminated correctly,
and 5xx you can attribute to a cause within minutes. DNS in front is in
`...aws.route53-routing-and-health-checks`; CDN/WAF in front in
`...aws.cloudfront-distributions` and `...aws.waf-and-shield`.

## 1. Which one
| | ALB (layer 7) | NLB (layer 4) | GWLB (layer 3, Geneve) |
|---|---|---|---|
| Routes on | host, path, header, query, method, source IP | port / protocol | everything (transparent bump-in-the-wire) |
| Targets | instance, IP, Lambda, **another ALB** | instance, IP, **ALB** | instance, IP (firewall appliances) |
| Static IP | no (use NLB → ALB, or Global Accelerator) | yes, one per AZ, EIP allowed | n/a (reached via GWLB endpoint) |
| TLS | terminate; mTLS; SNI multi-cert | terminate or pass-through TCP | pass-through |
| Extras | OIDC/Cognito auth, redirects, fixed responses, weighted TGs, gRPC, WebSockets, HTTP/2 | PrivateLink service, UDP, ~ms latency, millions of RPS, source IP preserved | appliance scaling, flow stickiness, endpoint service for other VPCs |
Internal vs internet-facing is chosen at creation and cannot be flipped. Put the
balancer in **public subnets of every AZ you run targets in** (at least two) — targets
in an AZ the LB is not in receive no traffic unless cross-zone is on.

## 2. Target groups and health checks
- Target type `instance` registers by instance id (auto-scaling friendly); `ip` is
  needed for Fargate/EKS pods, peered-VPC and on-prem (via DX/VPN) targets; `lambda`
  invokes a function; `alb` lets an NLB front an ALB for static IPs.
- Health check: protocol/path (`/healthz`), interval 30 s (min 5 for ALB, 10 for NLB),
  healthy/unhealthy thresholds, **success codes** (`200-299` or exact), and for ALB a
  per-target-group port override. Make `/healthz` cheap and dependency-aware; the
  default `/` on a redirecting app returns 301 and marks every target unhealthy.
- **Deregistration delay** (default 300 s, `deregistration_delay.timeout_seconds`)
  keeps in-flight requests alive after a target leaves — set it to your longest request
  (e.g. 30 s for an API) or deploys take five minutes per instance. NLB adds a
  `connection_termination` option to kill lingering TCP flows.
- **Slow start** (`slow_start.duration_seconds`, ALB) ramps new targets; **stickiness**
  (`stickiness.type` `lb_cookie` / `app_cookie` on ALB, `source_ip` on NLB) only when
  the app cannot share session state — it fights scaling.
- `target_group_health.dns_failover.minimum_healthy_targets.*` and
  `unhealthy_state_routing.*` decide when an AZ with few healthy targets is pulled from
  DNS or when traffic fails open to all targets — set them consciously for small groups.

## 3. Listeners and rules (ALB)
- One HTTPS listener per LB; HTTP listener with a single `redirect` to 443 (301).
- Rules evaluate by **priority** (1 = first); the default rule is last. Conditions can
  AND up to five types; actions: `forward` (with weighted target groups for canaries,
  `TargetGroupStickinessConfig` to keep a client on its canary), `redirect`,
  `fixed-response`, `authenticate-oidc`/`authenticate-cognito` then forward.
- TLS: attach an ACM certificate (`...aws.acm-certificates-and-private-ca`); add more
  with `add-listener-certificates` and SNI picks per hostname. Security policy
  `ELBSecurityPolicy-TLS13-1-2-2021-06` is the current sane default; FIPS variants exist.
  **mTLS**: `mutual-authentication-mode verify` with a trust store (CA bundle in S3),
  or `passthrough` to hand the client cert to the app in `X-Amzn-Mtls-Clientcert-*` headers.
- Attributes that matter: `idle_timeout.timeout_seconds` (default 60),
  `routing.http.drop_invalid_header_fields.enabled true`,
  `routing.http.desync_mitigation_mode defensive` (or `strictest`),
  `routing.http.xff_header_processing.mode`, `access_logs.s3.enabled` (bucket policy
  for the regional ELB account id or `logdelivery.elasticloadbalancing.amazonaws.com`),
  `connection_logs.s3.enabled` for TLS-handshake-level logs.
- HTTP/2 and gRPC are per target group protocol version (`HTTP2`, `GRPC`); WebSockets
  work automatically on HTTP/1.1 listeners.

## 4. NLB specifics
- Static IPv4 per AZ: pass `SubnetMappings` with `AllocationId` of EIPs; for internal
  NLBs `PrivateIPv4Address`. These are the addresses to give partners for allowlists.
- **Client IP preservation** is on by default for instance/IP targets in the same VPC
  — target security groups must then allow the *client* CIDR, not the NLB; off for
  PrivateLink and ALB targets. NLBs accept **security groups** (since 2023): enable
  `enforce_security_group_inbound_rules_on_private_link_traffic` deliberately.
- Health checks come from the VPC CIDR (not the NLB IPs) — allow it in target SGs.
- TLS listener: terminates with ACM cert and `TCP` back to targets, or `TLS` to
  re-encrypt; ALPN policy `HTTP2Preferred` for gRPC.
- Cross-zone is **off** by default for NLB and billed per GB when on; ALB has it on
  and free. Cross-zone can also be set per target group now.
- Expose a service via **PrivateLink**: NLB → `create-vpc-endpoint-service
  --network-load-balancer-arns` → consumers create interface endpoints; acceptance
  and principal allowlists control who.

## 5. Gateway Load Balancer
- Appliances (firewalls/IDS) register as targets on **Geneve port 6081**; traffic is
  steered to the GWLB through a **GWLB endpoint** in the consumer VPC using route-table
  entries (edge/ingress route table on the IGW for inbound inspection, subnet routes
  for east-west/egress). Flows stick to one appliance (5-tuple, or 3-tuple/2-tuple
  via `target_group_attributes`); `rebalance` on deregistration decides whether
  existing flows move. Appliance health = GWLB health check on the appliance's
  management port, not on Geneve.

## 6. Reading the 5xx
- **502 from ALB**: target closed the connection (keepalive shorter than the ALB idle
  timeout — set app keepalive to **> 60 s**, e.g. nginx `keepalive_timeout 75;`,
  Node `server.keepAliveTimeout = 65000`), malformed response, or Lambda target error
  / 1 MB response limit. `ELB 5XX` vs `Target 5XX` CloudWatch metrics separate these.
- **503**: no registered healthy targets; **504**: target did not respond within idle
  timeout; **460**: client closed before response (idle timeout on client side);
  **463**: more than 30 IPs in `X-Forwarded-For`. `error_reason` in access logs names
  it (`TargetTimeout`, `BadGateway`…).
- Sudden traffic spikes: ALB scales in minutes; pre-warm via Support for a known event,
  or put CloudFront/Global Accelerator in front. `RejectedConnectionCount` shows it.

## Gotchas
- ALB IPs change; never hardcode them — alias record only. Callers that cache DNS
  (Java) need TTL caps.
- Lambda targets receive requests as JSON events and must return the ALB response
  shape; health checks for Lambda targets invoke the function (billed).
- ALB access logs are off by default and are the only record of the real client IP
  when targets log the LB address; enable them before you need them.
- LCU pricing: an LB with tiny traffic still bills the hourly rate; dozens of
  per-microservice ALBs cost more than one ALB with host-based rules.
- Zonal shift (`arc-zonal-shift start-zonal-shift`) pulls one AZ from the LB in
  seconds for ALB/NLB with cross-zone **off** or with zonal autoshift enabled — plan
  capacity for n-1 AZs.

## Verify
- [ ] `/healthz` returns 200 only when dependencies are reachable; all targets healthy in every AZ the LB spans.
- [ ] Deregistration delay ≤ longest request; a rolling deploy produces zero 5xx in `HTTPCode_ELB_5XX_Count`.
- [ ] HTTP listener redirects to HTTPS; `ssllabs`-style scan shows TLS 1.2+ only and the intended cert chain.
- [ ] Access logs landing in S3 and queryable (Athena DDL from the AWS docs works).
- [ ] Backend keepalive > ALB idle timeout; `HTTPCode_ELB_502_Count` is flat under load.
