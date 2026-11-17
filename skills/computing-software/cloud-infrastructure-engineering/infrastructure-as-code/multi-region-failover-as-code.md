---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.multi-region-failover-as-code
name: multi-region-failover-as-code
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, disaster-recovery-iac, failover-as-code, multi-region, route53-failover, pilot-light, warm-standby, aurora-global-database, terraform, runbook-automation]
level: sme
status: draft
description: "Define multi-region standby and failover in code: region-parameterised stacks, data replication, health-checked DNS failover, a scripted promotion runbook, and failback."
sources: ["AWS Whitepaper - Disaster Recovery of Workloads on AWS: pilot light, warm standby, multi-site (https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/)", "Amazon Route 53 Developer Guide - DNS failover and health checks; Route 53 Application Recovery Controller", "Amazon Aurora User Guide - Global database switchover and failover"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-region failover as code

Goal: the secondary region is created by the same code as the primary, data replicates
continuously, and failover is a reviewed, scripted operation — not a war-room improvisation.

## 1. Choose the pattern (cost vs RTO)
| Pattern | Secondary region runs | Typical RTO |
|---|---|---|
| Backup & restore | Nothing; backups copied cross-region | hours |
| Pilot light | Data replicas + core infra, compute scaled to 0 | tens of minutes |
| Warm standby | Everything at reduced capacity | minutes |
| Active-active | Full capacity serving traffic | ~0 (routing) |

## 2. One stack, region as a parameter
```
live/prod/
  eu-west-1/app/   -> module "app" { region = "eu-west-1", role = "primary",   desired = 12 }
  eu-central-1/app/-> module "app" { region = "eu-central-1", role = "secondary", desired = var.dr_active ? 12 : 0 }
```
Same module version in both; CI plans both on every change so the secondary never rots.
Region-specific values (AMI IDs, AZ names, KMS keys, certificate ARNs) come from data sources
or per-region maps, never hard-coded in the module.

## 3. Data replication in code
- Aurora global database (`aws_rds_global_cluster` + secondary cluster), DynamoDB global tables (`replica {}` blocks), S3 cross-region replication rules, ECR replication, Secrets Manager replica regions, KMS multi-region keys.
- Things people forget: parameter store values, IAM is global but KMS/ACM/AMIs are regional, quotas in the secondary region (request increases ahead), container images and artifacts.

## 4. Traffic failover
```hcl
resource "aws_route53_health_check" "primary" {
  fqdn              = aws_lb.primary.dns_name
  type              = "HTTPS"
  resource_path     = "/healthz"
  failure_threshold = 3
  request_interval  = 10
}
resource "aws_route53_record" "api_primary" {
  zone_id = var.zone_id
  name    = "api.example.com"
  type    = "A"
  set_identifier = "primary"
  failover_routing_policy { type = "PRIMARY" }
  health_check_id = aws_route53_health_check.primary.id
  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }
}
# matching SECONDARY record pointing at the secondary LB
```
Automatic DNS failover handles compute/LB loss. **Data promotion stays a deliberate action** —
automatic database promotion on a flapping health check causes split brain. For controlled
switchover use Route 53 ARC routing controls or a feature flag in config.

## 5. The failover runbook as code
A pipeline/playbook with explicit, ordered, idempotent steps:
1. Freeze deploys; confirm primary is really down (multiple vantage points).
2. Promote data: `aws rds failover-global-cluster --global-cluster-identifier orders --target-db-cluster-identifier <secondary-arn>` (use `switchover-global-cluster` for planned, no-data-loss moves).
3. Scale secondary: apply with `dr_active = true` (pilot light/warm standby).
4. Shift traffic (ARC routing control / DNS weights) and verify smoke tests.
5. Communicate; record timeline.
Failback is a second runbook: re-establish replication toward the old primary, switchover back in a window.

## Gotchas
- A secondary region that is never exercised fails on the day: run the failover in game days (see game-day skill) at least twice a year.
- Terraform state for the secondary must not live only in the primary region's bucket; replicate the state bucket or keep the secondary's state in the secondary region.
- DNS TTLs and client caching (JVM DNS cache) delay traffic movement; keep TTL ≤ 60 s on failover records.

## Verify
- [ ] Plans for both regions are clean (no drift) on every merge.
- [ ] Last failover drill met the RTO/RPO targets with timings recorded; failback also tested.
