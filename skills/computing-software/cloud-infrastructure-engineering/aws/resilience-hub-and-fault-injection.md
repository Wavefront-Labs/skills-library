---
id: computing-software.cloud-infrastructure-engineering.aws.resilience-hub-and-fault-injection
name: resilience-hub-and-fault-injection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, resilience-hub, fault-injection, fis, chaos-engineering, resilience-assessment, resiliency-policy, fis-experiment-template, az-availability-power-interruption, stop-condition, rto-rpo-assessment]
level: practitioner
status: docs-checked
description: "Assess RTO/RPO with AWS Resilience Hub and test it with Fault Injection Service: experiment template parts, stop conditions on alarms, and the AZ power interruption scenario."
sources: ["https://docs.aws.amazon.com/resilience-hub/latest/userguide/setup-resiliency-policy.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/scheduled-assessment.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/run-assessment.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/resil-recs.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/resil-score.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/test-assessment-report.html", "https://docs.aws.amazon.com/fis/latest/userguide/experiment-templates.html", "https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html", "https://docs.aws.amazon.com/fis/latest/userguide/stop-experiment.html", "https://docs.aws.amazon.com/fis/latest/userguide/az-availability-scenario.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resilience Hub and Fault Injection Service: score it, then test it

**Goal:** a resiliency score against a written RTO/RPO policy, a list of recommendations,
and FIS experiments that test recovery, with stop conditions so the experiment does not
become the incident.

## 1. Resilience Hub
1. **Resiliency policy** holds RTO/RPO targets for infrastructure and for Availability Zone
   disruptions, plus optional Regional targets.
2. **Assess**: run from Applications > Actions > Assess resiliency, or from the Assessments
   tab with Run resiliency assessment. Run a new one when the application or policy changes.
3. **Daily assessment**: turn on "Automatically assess daily". It starts only after a first
   successful manual assessment and requires an appropriate IAM role. Daily runs count
   against your run quota.
4. **Drift notification**: turn on "Get notified when the application drifts" and give an
   SNS topic (same or another account/Region via ARN). The topic needs permissions that let
   Resilience Hub publish to it.
5. **Recommendations**: up to three options. Optimize for AZ RTO/RPO (or Region RTO/RPO
   when Regional targets are set), for cost, or for minimal changes. Each lists a
   description, changes, base cost and estimated workload RTO/RPO after the change.
6. **Resiliency score**: top score is 100. It reflects how closely you follow the
   recommended alarms, SOPs and tests. Excluding recommendations only changes the score
   after a new assessment.
- RTO/RPO values are estimates only. The guide says to test real recovery times yourself,
  for example with AWS FIS.
- If an AppComponent cannot meet the policy and no recommendation exists, change its
  resource type or adjust the policy to what the resource can deliver.

## 2. Resilience Hub to FIS
- Operational recommendations tab > Fault injection experiments lists recommended
  experiments with states Implemented, Partially implemented, Not implemented, Excluded.
- Choose an action, select AppComponents to include/exclude, then Initiate experiment. This
  opens the Specify template details page in the FIS console in a new tab; you finish
  creating the template there. You can add actions and targets manually to improve coverage.
- FIS scenarios are console-only; Resilience Hub cannot track them and shows state
  Not trackable.
- To have Resilience Hub detect the latest experiments you ran, run a new assessment.

## 3. FIS experiment template
Components: actions (run in a set order or simultaneously), targets, stop conditions,
experiment role (IAM), experiment report configuration, experiment options. Template top
level keys: `description`, `targets`, `actions`, `stopConditions`, `roleArn`,
`experimentReportConfiguration`, `experimentOptions`, `tags`.

**Stop conditions** are CloudWatch alarms. If one fires during a run, FIS stops the
experiment. A stopped experiment cannot be resumed.
```json
{"stopConditions":[{"source":"aws:cloudwatch:alarm","value":"arn:aws:cloudwatch:region:123456789012:alarm:alarm-name"}]}
```
`{"source":"none"}` means no stop condition. Define steady state first (latency, CPU,
retries) and build the alarm from it.

You can also stop a running experiment yourself (console Stop experiment, or the CLI
`stop-experiment` command). Any post actions not yet completed are completed first.

## 4. AZ Availability: Power Interruption scenario
Simulates complete power loss in one AZ for multi-AZ applications. Default: 30 minutes of
power-interruption symptoms, then 30 minutes of recovery symptoms. Actions with no matching
targets are skipped. Actions and their ids:
- Stop instances (`aws:ec2:stop-instances`), restarted afterwards; EKS pods and ECS tasks
  on them go away.
- Pause instance launches (`aws:ec2:api-insufficient-instance-capacity-error`), targeting
  IAM roles by ARN; pause ASG scaling (`aws:ec2:asg-insufficient-instance-capacity-error`).
- Pause network connectivity (`aws:network:disrupt-connectivity`) for 2 minutes on subnets.
- Failover RDS (`aws:rds:failover-db-cluster`).
- ElastiCache (`aws:elasticache:replicationgroup-interrupt-az-power`).
- Start ARC zonal autoshift (`aws:arc:start-zonal-autoshift`) five minutes in.
- Pause EBS I/O (`aws:ebs:pause-io`) on one volume.
- Disrupt connectivity to S3 Express One Zone directory buckets.

Targets are chosen by tag. Default tag key is `AzImpairmentPower` with per-action values
(for example `StopInstances`, `IceAsg`, `DisruptSubnet`, `DisruptRds`,
`ElasticacheImpact`, `RecoverAutoshiftResources`, `APIPauseVolume`); you can use your own
tags in the template.

## Gotchas
- The scenario has no stop conditions. Add your own to the experiment template.
- Fargate-run EKS pods and ECS tasks are not supported by the scenario.
- RDS Multi-AZ with two readable standby instances is not supported by the scenario.
- The experiment role needs the scenario's permissions policy attached; ARC creates the
  service-linked role for zonal autoshift when you create the template.
- Resilience Hub only recommends experiments and estimates; it does not prove recovery.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Dropped as unconfirmed on these pages: EventBridge drift alerting, an "application
(software)" disruption type, the full FIS action table beyond the scenario's, sample
template values, SCP and tag-condition advice, JVM DNS TTL, and game-day procedure.

## Verify
- [ ] An assessment has run and open recommendations have an owner.
- [ ] Every experiment template has a CloudWatch alarm stop condition (or an explicit decision not to).
- [ ] The AZ scenario target tags exist on the intended resources only.
