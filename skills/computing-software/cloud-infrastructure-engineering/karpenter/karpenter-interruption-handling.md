---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-interruption-handling
name: karpenter-interruption-handling
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [interruption, sqs, eventbridge, spot-interruption, interruption-queue, describeinstancestatus, rebalance-recommendation]
level: advanced
status: docs-checked
description: "Interruption handling: events handled, SQS queue and EventBridge requirement, --interruption-queue argument, status-check handling, and spot rebalance caveat."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter interruption handling

Karpenter watches for involuntary events and taints, drains and terminates the affected node ahead of time:
- Spot Interruption Warnings (2 minute notice)
- Scheduled Change Health Events (maintenance)
- Instance Terminating and Instance Stopping events
- Instance Status Check Failures

For spot warnings the NodePool starts a replacement as soon as the warning arrives while draining in parallel; average node startup is usually shorter than the 2 minutes.

Setup: provision an SQS queue plus EventBridge rules and targets forwarding those AWS events to it (the getting-started CloudFormation template does this), then run the controller with `--interruption-queue` set to the queue name.

Separate path: Karpenter calls EC2 `DescribeInstanceStatus` to find unhealthy instances (System Status, Instance Status, Scheduled Maintenance Events). This needs only the IAM permission, not the queue.

Spot Rebalance Recommendations: Karpenter publishes Kubernetes events but does not taint, drain or terminate for them. If needed, run AWS Node Termination Handler alongside, accepting more node churn since NTH cordons and drains on rebalance recommendations.

Interruption is forceful: it ignores NodePool budgets and `karpenter.sh/do-not-disrupt`, though it has an implicit upper bound on termination time.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. Removed the INTERRUPTION_QUEUE environment variable name, which the page does not state.
