---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.game-days-and-chaos-drills-for-infrastructure
name: game-days-and-chaos-drills-for-infrastructure
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, disaster-recovery-iac, game-day, chaos-day, chaos-engineering, aws-fis, azure-chaos-studio, rebuild-drill, resilience-testing]
level: sme
status: draft
description: "Plan and run infrastructure game days: hypotheses, blast radius and abort criteria, fault injection with AWS FIS or Chaos Studio, rebuild-from-code drills, and turning findings into code fixes."
sources: ["AWS Well-Architected Reliability Pillar - Conduct game days regularly (REL12-BP05) (https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)", "AWS Fault Injection Service User Guide (https://docs.aws.amazon.com/fis/latest/userguide/)", "Principles of Chaos Engineering (https://principlesofchaos.org/) and Google SRE Book - Testing for reliability / DiRT"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Game days and chaos drills for infrastructure

Goal: prove, on a calendar date, that failover, alarms, runbooks and rebuild-from-code actually
work — and find the gaps while everyone is awake and watching.

## 1. Plan (2–3 weeks before)
- **Scope and hypothesis**: "If one AZ loses all EC2 instances, the ASG restores capacity in the other AZs within 10 minutes and p99 latency stays < 800 ms."
- **Blast radius**: start in stage; in prod, limit by tag (`chaos=allowed`), percentage, or one AZ.
- **Abort criteria** (written): SLO burn > X, customer-facing errors > Y, any data-integrity alarm → stop and roll back.
- **Roles**: facilitator, operators (on-call who would really respond), observers/scribe, decision-maker for abort. Inform support and stakeholders.
- **Steady-state metrics** dashboard ready; check alarms are routed.

## 2. Inject faults (as code, repeatable)
AWS FIS experiment template (Terraform `aws_fis_experiment_template` or JSON):
```json
{
  "description": "Stop 50% of app instances in one AZ",
  "targets": {"app": {"resourceType": "aws:ec2:instance",
    "resourceTags": {"app": "orders", "chaos": "allowed"},
    "filters": [{"path": "Placement.AvailabilityZone", "values": ["eu-west-1a"]}],
    "selectionMode": "PERCENT(50)"}},
  "actions": {"stop": {"actionId": "aws:ec2:stop-instances", "targets": {"Instances": "app"},
    "parameters": {"startInstancesAfterDuration": "PT15M"}}},
  "stopConditions": [{"source": "aws:cloudwatch:alarm", "value": "arn:aws:cloudwatch:eu-west-1:<ACCOUNT_ID>:alarm:orders-slo-burn"}],
  "roleArn": "arn:aws:iam::<ACCOUNT_ID>:role/fis-experiments"
}
```
Stop conditions on CloudWatch alarms implement the abort criteria automatically.
Azure Chaos Studio experiments (VM shutdown, AKS Chaos Mesh faults, NSG rules) are the
equivalent; Kubernetes: Chaos Mesh / Litmus. Other scenarios: DNS failure, dependency latency
(`aws:ssm:send-command` with tc netem), credential expiry, region failover (see failover skill).

## 3. Rebuild drill (IaC-specific)
Destroy and recreate a non-prod environment from code, timed, with only the repo, pipeline and
documented secrets: measures real RTO and surfaces hidden manual steps (console-created DNS,
untracked IAM, hand-loaded secrets, quotas).

## 4. Run and record
Timeline with timestamps: injection, first alert, human acknowledgement, mitigation, recovery.
Compare with the hypothesis. Abort without hesitation if criteria hit.

## 5. Follow-up
Blameless review within a week; every finding becomes a ticket with owner — ideally a code
change (missing alarm in Terraform, ASG health check type, runbook automated as an Ansible
playbook). Re-run the same experiment to prove the fix; schedule quarterly.

## Gotchas
- Chaos without observability is just an outage; confirm you can see steady state before injecting.
- FIS role permissions too broad = experiments can hit untagged resources; scope by tag in the IAM policy too.
- Don't run during peak or change freezes; coordinate with other teams' deployments.

## Verify
- [ ] Hypothesis confirmed or refuted with metrics; timeline and findings documented.
- [ ] Follow-up tickets closed and the experiment re-run successfully.
