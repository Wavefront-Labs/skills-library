---
id: computing-software.cloud-infrastructure-engineering.aws.deep-vs-shallow-health-checks
name: deep-vs-shallow-health-checks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, health-checks, elb, alb, route53, resilience, builders-library, deep-health-check, shallow-health-check]
level: advanced
status: docs-checked
description: "Design health checks that drop bad hosts without fleet-wide outages: shallow vs local vs dependency checks, ALB fail-open and sensible check settings."
sources: ["https://aws.amazon.com/builders-library/implementing-health-checks/", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Deep vs shallow health checks

## 1. Definitions (Builders' Library terms)
- **Liveness**: is the process up and able to answer? Cheap, never touches dependencies.
- **Local health check**: tests resources not shared with the server's peers (disk, worker pool, local config),
  so it is unlikely to fail on many servers at once.
- **Dependency health check**: also tests shared dependencies such as the database. Thorough but dangerous.

## 2. The core risk
A dependency check can cause a cascading failure: if the shared dependency blips, every host may fail its
check at once. Failing checks when only one code path is unhealthy also widens the scope of impact (for example a
read API that serves cached data while the database is down).

## 3. Guidance from the Builders' Library
- Configure the work producer (load balancer, queue-polling thread) to run liveness and local checks only, so servers
  leave service only for problems definitively local to them, such as a bad disk.
- Run dependency checks and anomaly detection from external monitoring systems that alarm or engage an operator
  (or terminate instances), not from the load balancer.
- An external system can judge a server's health more accurately than the server itself; teams using Auto Scaling
  configure external ping checks and sometimes a custom checker that saves state so it does not mark too many
  servers unhealthy at once.

## 4. Fail-open behaviour
- **ALB**: if a target group contains only unhealthy targets, the load balancer routes requests to all of them
  regardless of health, so when all targets fail at the same time in all enabled AZs it fails open.
- Fail-open does not rescue you from a system that terminates or replaces unhealthy hosts: check what your
  Auto Scaling or orchestrator health checks do before adding any dependency check.

## 5. ALB target group settings (from the target-group health check page)
`HealthCheckPath` defaults to `/`; `HealthCheckTimeoutSeconds` range 2-120, default 5 (instance/ip targets);
`HealthCheckIntervalSeconds` range 5-300, default 30; `HealthyThresholdCount` range 2-10, default 5;
`UnhealthyThresholdCount` range 2-10, default 2. Tune to detect a bad host quickly without flapping.
```python
# /health (liveness + local state, used by the load balancer)
@app.get("/health")
def health():
    if not local_state.ready or disk_free_pct() < 5:
        return Response(status_code=503)
    return {"status": "ok"}

# /health/deep (dependencies, used by canaries and dashboards only)
@app.get("/health/deep")
def deep():
    return {"db": db_ping_cached(), "payments": payments_ping_cached()}
```

## Verify
- [ ] A simulated DB outage in staging does not mark hosts unhealthy or replace them.
- [ ] A host with a full disk or crashed worker pool leaves the target group within threshold x interval.
- [ ] Dependency status is visible on dashboards or canaries and alarmed separately.

## Checked
2026-10-28. Confirmed on the Builders' Library article and the ALB target-group health check page: local vs
dependency checks, cascading-failure risk, load balancer scope guidance, fail-open behaviour, parameter ranges and
defaults. Removed (not confirmed on the pages): NLB fail-open, Route 53 fail-open, the
`target_group_health.unhealthy_state_routing` attribute names, ASG/ECS termination behaviour and
`HealthCheckType`/`startPeriod`/slow start/grace-period advice, and the 2-3 threshold and 10-15 s interval values.
Method: documentation only; no commands were run.
