---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.pre-scaling
name: pre-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, scalability, pre-scaling, pre-warming, peak-event-readiness, scaling-lag, scheduled-scaling, lb-pre-warming, provisioned-concurrency, warm-pools, event-readiness]
level: practitioner
status: docs-checked
description: "Prepare for spikes that outrun autoscaling: compare scaling lag to the expected ramp, then use warm pools, Lambda provisioned concurrency and ALB capacity unit reservations."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html", "https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/capacity-unit-reservation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-scaling for events

Autoscaling reacts after load arrives; a marketing email or a kickoff time can ramp faster than new capacity
becomes ready.

## Steps
1. **Measure scaling lag** per tier from your own data (alarm evaluation, instance or container start,
   application warm-up, health checks). Compare it with the expected ramp. If the ramp is faster, pre-scale.
2. **Pick the tool per tier**:
   - **EC2 Auto Scaling warm pools** reduce latency for applications with exceptionally long boot times.
     AWS warns that a warm pool nobody needs adds cost; skip it if first-boot time causes no noticeable
     latency.
   - **Lambda provisioned concurrency** keeps pre-initialised execution environments ready, reducing cold
     start latency. It suits interactive workloads and usually not asynchronous pipelines. It incurs
     additional charges, unlike reserved concurrency, which both guarantees and caps concurrency.
   - **ALB capacity unit (LCU) reservation** sets a static minimum capacity; the load balancer still scales
     above it. AWS lists an upcoming high-traffic event, short unpredictable spikes, a cut-over at a set
     start time and matching a source load balancer during migration as use cases. The minimum request is
     100 LCU; the maximum depends on account quotas.
   - Estimate LCU needs from load tests or history. AWS recommends the CloudWatch `PeakLCUs` metric (a
     per-minute Sum) rather than `ConsumedLCUs`, which covers only billing dimensions.
3. **Check downstream limits** such as third-party APIs and payment providers, and your own quotas.
4. **Event runbook**: timeline, owners, dashboards, stop and rollback criteria, and a scheduled scale-down so
   pre-scaled capacity does not stay on after the event.

## Gotchas
- Forgetting downstream dependencies.
- Leaving pre-scaled capacity running after the event.

## Verify
- [ ] A rehearsal load test at the expected ramp passes before the event.

## Checked
2026-11-01. Confirmed against the EC2 Auto Scaling warm pools page, the Lambda provisioned concurrency page
and the ALB capacity reservation page. Removed: typical boot-time ranges, Kubernetes overprovisioning,
Cloud Run and Container Apps minimum instances, database and cache pre-warming advice and the AWS
Infrastructure Event Management reference (its page was not read), none of which these pages state.
Method: documentation only; no commands were run.
