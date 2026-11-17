---
id: computing-software.cloud-infrastructure-engineering.aws.global-accelerator-multi-region-failover
name: global-accelerator-multi-region-failover
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, global-accelerator, ga-failover, active-passive, traffic-dial, health-checks]
level: advanced
status: gated
description: "Build active-passive multi-Region failover with Global Accelerator endpoint groups, health checks and traffic dials, and automate the dial flip."
sources: ["https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups-traffic-dial.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups-health-check-options.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/disaster-recovery-resiliency.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global Accelerator failover for multi-Region active-passive

## 1. Building blocks
- One endpoint group per Region under a listener; endpoints (ALB/NLB/EC2/EIP) carry weights (0-255).
- **Health checks**: ALB/NLB endpoints use the load balancer's own target health; for EC2/EIP endpoints
  the endpoint group's health check applies (protocol, port, interval 10 to 30 s, threshold count 1 to 10).
- **Traffic dial** (0-100, default 100) per endpoint group controls the percentage of traffic directed to that
  group. It applies only to traffic already directed to the group and only to new connections.
- Global Accelerator monitors all endpoints and routes only to healthy, active ones; with no healthy
  endpoint it routes to all endpoints in the group.

## 2. Active-passive
Set the primary group's dial to 100 and the standby group's dial to 0 (a dial of 0 cuts off traffic for that
Region; health checks are not affected by dial settings). To fail over, flip them explicitly:
```bash
aws globalaccelerator update-endpoint-group --region us-west-2 --endpoint-group-arn <STANDBY_ARN> --traffic-dial-percentage 100
aws globalaccelerator update-endpoint-group --region us-west-2 --endpoint-group-arn <PRIMARY_ARN> --traffic-dial-percentage 0
```
`--region us-west-2` for Global Accelerator calls: (gated: unconfirmed, source is paywalled or blocked).
The traffic dial is also the documented way to take a Region out for an upgrade or maintenance
(dial to 0, then back to 100) and to test blue/green releases across Regions.

## 3. Stateful apps
`ClientAffinity: SOURCE_IP` sends all requests from one client source IP to the same endpoint. Keep sessions
shared or re-creatable, since failover moves users.

## Verify
- [ ] Failing the primary ALB's targets (FIS or scale to zero) shifts traffic to the standby group.
- [ ] Dial-flip runbook timed in a game day.

## Checked
2026-10-28: Confirmed against the Global Accelerator Developer Guide pages about-endpoint-groups-traffic-dial, about-endpoint-groups-health-check-options, about-endpoints and about-listeners, and the botocore model (UpdateEndpointGroup/CreateEndpointGroup ranges). Read end to end. Gated: the us-west-2 control-plane Region (no readable page states it). Removed as unconfirmed: the active-active nearest-group behaviour, "within a minute" shift time, Route 53 ARC/Lambda automation, NewFlowCount metric, and the claim that failover moves SOURCE_IP-pinned users.

Method: documentation only; no commands were run.
