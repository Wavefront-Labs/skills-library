---
id: computing-software.cloud-infrastructure-engineering.aws.dns-based-disaster-recovery-failover
name: dns-based-disaster-recovery-failover
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, disaster-recovery, dns-failover, route53, failover-routing, health-checks, route53-arc]
level: practitioner
status: docs-checked
description: "DNS-based DR failover with Route 53: failover records with health checks, TTL choice, alarm-based and calculated checks, manual control with ARC, and client caching effects."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS-based DR failover

## Failover records
```json
{"Name":"app.example.com","Type":"A","SetIdentifier":"primary","Failover":"PRIMARY",
 "AliasTarget":{"HostedZoneId":"<ELB_HOSTED_ZONE_ID>","DNSName":"primary-alb-123.eu-west-1.elb.amazonaws.com","EvaluateTargetHealth":true},
 "HealthCheckId":"<hc-primary>"}
{"Name":"app.example.com","Type":"A","SetIdentifier":"secondary","Failover":"SECONDARY",
 "AliasTarget":{"HostedZoneId":"<ELB_HOSTED_ZONE_ID>","DNSName":"dr-alb-456.us-west-2.elb.amazonaws.com","EvaluateTargetHealth":true}}
```
- Route 53 answers with PRIMARY while it is healthy, SECONDARY otherwise.
- Alias to ELB with `EvaluateTargetHealth` uses the load balancer's target health; add an explicit health check for application-level health.

## Health checks
| Type | Use |
|---|---|
| Endpoint (HTTPS, string match) | `/health/deep` that checks critical dependencies; 10 or 30 s interval and a failure threshold |
| CloudWatch alarm | private endpoints or business metrics (error rate) |
| Calculated | combine children (e.g. healthy if 2 of 3 checks pass) |
- Health checkers run from multiple AWS regions; allow their IP ranges to the endpoint.
- Avoid health checks that fail when one non-critical dependency fails: you will fail over for nothing.

## Manual control
Automatic DNS failover can flap. Many teams prefer a **manual** decision with **Route 53 ARC
routing controls**, or invert a health check (`--inverted`) as a crude switch.

## TTL and clients
- Alias records use the target's TTL; for non-alias records set a low TTL on failover names.
- Clients and resolvers may cache longer: JVM DNS caching, connection pools that keep sockets open, mobile apps. Plan for minutes, and close idle connections on failover.

## Data side
DNS only moves traffic. The DR region's database must be writable (promoted) before or as traffic arrives; sequence it in the runbook.

## Verify
- [ ] Failing the primary health check (block health path) switches resolution within TTL + check interval x threshold.
- [ ] `dig app.example.com` from several networks shows the secondary; app works there.
- [ ] Failback tested.

## Checked

2026-10-28

Confirmed: 10 or 30 second check interval and failure threshold (Route 53 health-check page); EvaluateTargetHealth on alias targets, Inverted, HealthThreshold, ChildHealthChecks and AlarmIdentifier for calculated and CloudWatch-alarm checks (botocore route53).

Removed: hard-coded hosted zone IDs (now placeholders), failure threshold of 3, ARC routing-control description, 60 s ELB TTL figure, JVM property name, Global Accelerator claim.

Method: documentation only; no commands were run.
