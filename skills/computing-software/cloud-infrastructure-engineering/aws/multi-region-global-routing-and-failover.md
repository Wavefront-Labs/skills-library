---
id: computing-software.cloud-infrastructure-engineering.aws.multi-region-global-routing-and-failover
name: multi-region-global-routing-and-failover
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, multi-region, global-routing, regional-failover, route53, route53-arc, routing-controls, region-switch, global-accelerator, cloudfront-origin-failover, active-passive, active-active, health-checks]
level: advanced
status: gated
description: "Steer users between AWS Regions and fail over safely: Route 53 failover/latency records, ARC routing controls, Global Accelerator traffic dials, CloudFront origin groups."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html", "https://docs.aws.amazon.com/r53recovery/latest/dg/routing-control.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups-traffic-dial.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/high_availability_origin_failover.html", "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global routing and regional failover

**Goal:** users reach the nearest healthy Region; when a Region is impaired, traffic moves
to the other one by a decision you control (automatic or one switch), with a mechanism
that itself does not depend on the impaired Region.

## 1. Choose the steering layer
| Layer | Moves traffic via | Failover speed | Notes |
|---|---|---|---|
| Route 53 failover/latency/weighted records + health checks | DNS answers | TTL + health-check interval (TTL plus health-check detection time) | Clients caching DNS longer than TTL lag behind |
| **Route 53 ARC routing controls** | On/off switches that drive health checks | Same as DNS, but human-decided and data-plane-only | Highly available cluster across 5 Regions |
| **Global Accelerator** | Anycast IPs, endpoint-group traffic dials | Seconds; no DNS caching issue | TCP/UDP; static IPs; per-hour + DT premium |
| CloudFront origin groups | Per-request origin failover on 5xx/timeouts | Per request | GET/HEAD/OPTIONS only; good for static/read paths |

## 2. Route 53 active-passive
```json
{"Name":"api.example.com","Type":"A","SetIdentifier":"primary","Failover":"PRIMARY",
 "AliasTarget":{"HostedZoneId":"<ALB_ZONE>","DNSName":"alb-use1.example.elb.amazonaws.com","EvaluateTargetHealth":true},
 "HealthCheckId":"<HC_USE1>"}
```
plus a `SECONDARY` record for the other Region. Health checks should hit a **deep health
endpoint** (dependencies checked) through the public path; use calculated health checks to
combine signals. Active-active: latency records per Region with health checks on each.

## 3. ARC routing controls (human-in-the-loop failover)
```bash
aws route53-recovery-control-config create-cluster --cluster-name prod
aws route53-recovery-control-config create-routing-control --cluster-arn <CLUSTER> --routing-control-name use1
aws route53-recovery-control-config create-routing-control --cluster-arn <CLUSTER> --routing-control-name usw2
aws route53 create-health-check --caller-reference use1-rc-1 --health-check-config Type=RECOVERY_CONTROL,RoutingControlArn=<USE1_RC>
# failover: use the cluster's data-plane endpoints, not the control-plane API
aws route53-recovery-cluster update-routing-control-states --endpoint-url <CLUSTER_ENDPOINT> --region <ENDPOINT_REGION> \
  --update-routing-control-state-entries RoutingControlArn=<USE1_RC>,RoutingControlState=Off RoutingControlArn=<USW2_RC>,RoutingControlState=On
```
- Add **safety rules** (assertion: at least one Region On) so a fat-finger cannot black-hole
  everything.
- Keep the five cluster endpoints and credentials in the runbook; try endpoints in turn.
- ARC **Region switch** (newer) orchestrates multi-step Region failover plans (scaling,
  database promotion, routing) — evaluate it when the failover has many steps.
- Clusters bill per hour; one cluster can serve many applications.

## 4. Global Accelerator
One endpoint group per Region with ALB/NLB/EC2/EIP endpoints. Shift traffic with the
**traffic dial** (`update-endpoint-group --traffic-dial-percentage 0` drains a Region);
endpoint weights within a group. Health checks are GA's own; failover is automatic for
unhealthy endpoints.

## 5. Failover decision rules
- Automatic failover for clear signals (Region unreachable); manual (ARC switch) for gray
  failures, because flapping between Regions with stateful data is worse than a short outage.
- Fail over the data tier first (promote replicas) or at least confirm it before routing
  writes; see the multi-region data and DR skills
  (`computing-software.cloud-infrastructure-engineering.aws.disaster-recovery-strategies`).
- Failback is a separate, rehearsed change, not a reversal of the switch.

## Gotchas
- Editing Route 53 records during an incident uses the Route 53 control plane (a shared control plane that can be impaired during a large event (gated: unconfirmed, source is paywalled or blocked)); health-check and routing-control state changes are data plane. Pre-build
  records and flip with health checks/controls.
- Clients and resolvers ignoring TTL (JVM DNS cache, mobile apps) keep hitting the old
  Region; set `networkaddress.cache.ttl` and prefer GA for such clients.
- Health checkers on a public endpoint need SG/WAF allowlisting of Route 53 health-checker
  IP ranges.

## Verify
- [ ] Game day: turn the primary routing control Off; `dig api.example.com` returns the secondary within TTL plus detection time; synthetic canaries stay green.
- [ ] Safety rule blocks turning both controls Off.
- [ ] GA traffic dial to 0% on one Region drains it with no client errors.
- [ ] Runbook lists cluster endpoints and was executed from a laptop without console access.

## Checked

Date: 2026-11-02. Confirmed on Route 53 DNS failover, Route 53 ARC routing control, Global Accelerator traffic dial, CloudFront origin failover and the AWS DR whitepaper pages in sources, and by check_commands: failover/routing-control/traffic-dial concepts and CLI flags. Removed as not stated there: 1-3 minute detection time, ~1 minute game-day margin, the us-east-1 control-plane home (reworded and gated).

Method: documentation only; no commands were run.
