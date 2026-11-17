---
id: computing-software.systems-network-administration.backup-and-recovery.aws-elastic-disaster-recovery
name: aws-elastic-disaster-recovery
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [elastic-disaster-recovery, aws-drs, aws, replication-agent, cloud-dr, failback]
level: advanced
status: docs-checked
description: "Use AWS Elastic Disaster Recovery to replicate servers to AWS: staging area, agent, drills, recovery vs failover vs failback, recovery plans and failback mechanisms."
sources:
  - https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html
  - https://docs.aws.amazon.com/drs/latest/userguide/agent-installation.html
  - https://docs.aws.amazon.com/drs/latest/userguide/failback.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Elastic Disaster Recovery (DRS)

AWS Elastic Disaster Recovery replicates on-premises or cloud-based applications on supported operating
systems into your AWS account, to cut downtime and data loss using affordable storage, minimal compute and
point-in-time recovery.

## How it works
- Replication goes to a **staging area subnet** in your AWS account, in the Region you select. The staging
  design keeps cost down with affordable storage and minimal compute for ongoing replication.
- Use the AWS Management Console to configure replication and launch settings, monitor replication, and
  launch instances for drills or recovery.
- When you launch drill or recovery instances, the service automatically converts your servers to boot and
  run natively on AWS.
- Launch can use the most up-to-date server state or a previous point in time.
- After workloads run on AWS you can keep them there, or start replicating back to the primary site when the
  issue is resolved.

## Agent
Install the **AWS Replication Agent** on every source server you want to protect. The agent installation page
covers: generating the required AWS credentials, using an instance profile for installation in AWS, installation
instructions, installing on a secured network, uninstalling, reinstalling and supporting marketplace licences.
Follow the current instructions and supported-OS lists on that page; this skill does not reproduce installer
commands.

## Terms (from the recovery and failback page)
| Term | Meaning |
|---|---|
| Recovery | Launching recovery instances on AWS (console "Initiate recovery job" or the `start-recovery` API); creates new EC2 instances from replicated data. |
| Recovery drill | A non-disruptive test that launches drill instances; same process as recovery, no effect on source servers or ongoing replication. |
| Failover | Redirecting production traffic to the recovery instances. Done outside DRS, typically with a DNS routing service such as Route 53 or your traffic management. |
| Failback | Returning workloads from AWS to the original source infrastructure; DRS helps by replicating data from recovery instances back to the source servers. |

## Recovery and drills
- Drill and recovery instances can be launched once source servers are in Continuous Data Protection. After
  the initial sync completes you can customise the recovery environment ahead of an event.
- Drill and recovery instances launch similarly but serve different purposes; AWS recommends periodic drills
  during normal operations.
- To recover interdependent servers in a defined order with wait times between groups, use a **recovery plan**.

## Failback mechanisms
| Source infrastructure | Mechanism |
|---|---|
| On-premises | Failback Client ISO, or DRS Failback Automation. |
| AWS, same account | Start Reverse Replication on the Protected Recovery Instance. |
| AWS, cross account | Start Reverse Replication on the Protected Recovery Instance in the Failover Account. |
| Other cloud | Varies per provider. |

## Not covered here
Replication settings values, launch template options, ports, costs and exact installer commands are on
other DRS pages (replication settings, launch settings, network requirements); look them up there.

## Verify
Run periodic drills, record boot success and time to launch against your RTO, and test the failover step
(traffic redirection) separately because DRS does not perform it.

## Checked
Checked 2026-11-08 against What is Elastic Disaster Recovery, Installing the AWS Replication Agent (topic list
only; its body was not readable) and Using Elastic Disaster Recovery for recovery and failback.
Confirmed: staging area, console role, conversion at launch, terminology, recovery plans, failback table.
Removed because the cited pages do not state them: replication server and volume choices, installer command and
credentials flags, launch-template options, point-in-time ransomware claim, TCP ports, cost notes.
Method: docs-only read of cited pages, 2026-11-08
