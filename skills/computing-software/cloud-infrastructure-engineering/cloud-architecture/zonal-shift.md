---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.zonal-shift
name: zonal-shift
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, fault-isolation, zonal-shift, az-evacuation, route53-arc, zonal-autoshift, gray-failure, availability-zone-impairment]
level: practitioner
status: docs-checked
description: "Evacuate traffic from an impaired availability zone with AWS ARC zonal shift and autoshift: capacity to absorb the shift, per-zone signals and practice runs."
sources: ["https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-shift.html", "https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-autoshift.html", "https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-shift.resource-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zonal shift and AZ evacuation

## Why
Gray failures (elevated latency/errors in one zone) often don't fail health checks cleanly. You need
a deliberate lever to move traffic away from a zone, then move it back.

## Mechanisms
- **AWS ARC zonal shift**: shifts traffic for an opted-in resource away from an impaired AZ to
  healthy AZs in the same Region. Supported resources: EC2 Auto Scaling groups, EKS, and
  Application and Network Load Balancers (cross-zone enabled or disabled). Every shift is
  temporary: you set an expiry from 1 minute up to 3 days (72 hours), can extend it, and can
  cancel it at any time.
- **Zonal autoshift**: you authorise AWS to shift traffic when its own telemetry shows an AZ
  impairment. ARC does not inspect the health of individual resources, so traffic may be shifted
  for resources that are not affected. Practice runs are required, run weekly, shift one
  resource away for about 30 minutes and report an outcome such as SUCCEEDED or FAILED.
- Other platforms: this skill's sources cover AWS only; look up the equivalent lever for your
  platform in its own documentation.

## Prerequisites
1. **Capacity**: pre-scale every AZ so the remaining zones can absorb the load. Do not rely on
   scaling during the event; autoshift and practice runs do not wait for auto scaling. If you
   use auto scaling, set the minimum capacity so the app runs normally without one AZ.
2. Opt the resource in and make sure it is active and fully provisioned; check IAM permissions.
3. Per-zone observability: ALB and NLB publish per-AZ CloudWatch metrics; use them to confirm traffic drains.
4. Connection reuse can keep traffic flowing to the shifted-away AZ longer than expected; limit how long clients stay connected.
5. If several load balancers share targets, a shift on a cross-zone enabled load balancer drops target capacity for all of them.

## Steps
1. Detect a zone outlier (per-AZ metrics, provider health events).
2. Prescale, then start the zonal shift for the resource and AZ; confirm traffic and errors drop.
3. Monitor remaining zones' saturation.
4. Cancel or let the shift expire once the zone is healthy; observe.

## Verify
- [ ] Start a zonal shift before enabling autoshift to test the app runs without one AZ.
- [ ] Practice runs report SUCCEEDED (EventBridge notifications can alert on autoshifts and practice runs).

## Checked
2026-11-08
Method: documentation only; no commands were run.
Confirmed against the ARC Developer Guide pages Zonal shift, Zonal autoshift and Supported resources. Removed: Azure and Kubernetes mechanism bullets and the data-tier prerequisite (not stated in cited pages), and the static-stability article as a source.
