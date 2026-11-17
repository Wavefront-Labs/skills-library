---
id: computing-software.systems-network-administration.backup-and-recovery.pilot-light-and-warm-standby-in-cloud
name: pilot-light-and-warm-standby-in-cloud
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pilot-light, warm-standby, cloud-dr, multi-site-active-active, route-53-failover, disaster-recovery]
level: advanced
status: docs-checked
description: "Design cloud DR as pilot light or warm standby: what runs continuously, data replication, scale-out and failover on invocation, trade-offs and testing."
sources:
  - https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html
  - https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pilot light and warm standby in the cloud

**Goal:** choose the cheapest DR pattern that meets the workload's RTO and RPO.

## The spectrum (AWS DR whitepaper terms)
| Strategy | Running in DR region | Notes |
|---|---|---|
| Backup and restore | Backups (and replicated data) only; infrastructure, configuration and code redeployed on recovery | Suits data loss or corruption; use IaC so redeploy is quick and error-free |
| Pilot light | Data replicated; core infrastructure such as databases and object storage always on; application servers loaded with code and configuration but switched off | Minimises ongoing cost; cannot process requests until switched on and scaled out |
| Warm standby | Scaled-down but fully functional copy of production, always on | Handles traffic at reduced capacity immediately; only needs scale-up |
| Multi-site active/active | Workload serving traffic from several Regions | Most complex and costly; near-zero recovery time for most disasters, but data corruption still relies on backups |

Use your RTO and RPO needs to choose. For disruption of a single data center a well-architected highly available workload may need only backup and restore; consider the other three if a disaster means loss of a Region or regulation requires it.

## Pilot light build
- Continuous cross-region replication of data: AWS lists S3 Replication, RDS read replicas, Aurora global databases, DynamoDB global tables, DocumentDB global clusters and ElastiCache Global Datastore. Replication alone does not protect against corruption or deletion, so add versioning or point-in-time backups, including in the DR Region.
- Promoting an RDS read replica (non-Aurora) takes a few minutes and includes a reboot. AWS states an Aurora global database secondary can be promoted in under a minute.
- Golden AMIs copied to both Regions, and infrastructure as code (for example CloudFormation) that deploys the full stack in the primary Region and a scaled-down or switched-off stack in the DR Region. AWS recommends not deploying a "switched off" resource at all, and building the configuration to deploy it when needed. It also recommends a separate account per Region for isolation.
- Deploy workload changes to every Region at the same time.

## Warm standby build
Everything from pilot light, with the application tier already running at reduced size. Scale out the Auto Scaling group desired capacity on invocation. Ensure service quotas in the DR Region are high enough to reach production capacity. Auto Scaling is a control plane activity, so depending on it lowers resiliency; provisioning full capacity in advance is called hot standby.

## Traffic failover
- Route 53 health checks with DNS failover (a data plane operation). For manual failover, Amazon Application Recovery Controller (ARC) routing controls act as on/off health checks you control through a data plane API; changing weighted routing weights is a control plane operation and less resilient.
- AWS Global Accelerator is the other option AWS describes; it avoids DNS caching issues.
- AWS cautions that automatic failover on health checks should be used with care because a false alarm incurs real losses. Manual initiation is common, with the steps automated so initiation is a button push.

## Testing
Regularly test the strategy; AWS notes it is critical. For active/active, test how the workload reacts to loss of a Region and that the remaining Regions can take all traffic. Test data-disaster recovery from backups too.

## Gotchas
- Quotas and capacity in the DR region are a classic failure; request increases in advance.
- Configuration drift between regions breaks pilot lights silently; deploy to all Regions from the same pipeline.

## Verify
Last game day achieved RTO and RPO within targets, with the timeline recorded.

## Checked

2026-11-09. Confirmed against the AWS whitepaper "Disaster recovery options in the cloud" (four strategies and their definitions, replication services, RDS promotion and Aurora global database under-one-minute promotion, IaC and AMI guidance, separate accounts, Auto Scaling desired capacity and quotas, hot standby, Route 53/ARC/Global Accelerator, caution on automatic failover) and the Route 53 health checks page (opening only; health check types). Removed: RTO/RPO time ranges, Azure SQL geo-replication, Azure Site Recovery, Traffic Manager and Front Door, the 60-second TTL and "1 instance per tier" figures (not on cited pages).

Method: documentation only; no commands were run.
