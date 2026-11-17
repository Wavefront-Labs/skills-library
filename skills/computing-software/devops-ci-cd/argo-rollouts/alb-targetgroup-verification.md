---
id: computing-software.devops-ci-cd.argo-rollouts.alb-targetgroup-verification
name: alb-targetgroup-verification
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [aws, alb, targetgroup, aws-verify-target-group, ip-mode, readiness-gates, argo-rollouts]
level: sme
status: docs-checked
description: "Enable TargetGroup IP and weight verification so AWS ALB updates do not scale down old pods too early."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/alb/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rollouts can double-check AWS state before scaling down, via two checks.

**IP verification** (since v1.1) applies when the AWS Load Balancer Controller runs in IP mode (pod IPs registered). Service selector changes cannot get readiness gates injected because pods already exist, so if registration of the new pod IPs is delayed, scaling down the old ReplicaSet leaves the target group pointing at dead IPs and causes 502 errors. With verification on, whenever a service selector changes, the controller blocks progress until all pod IPs in the `bluegreen.activeService` Endpoints list are registered in the TargetGroup. Verification must succeed before `postPromotionAnalysis` runs or the old ReplicaSet is scaled down.

**Weight verification** (since v1.0) applies in IP or instance mode. After a `setWeight` step it queries the ALB APIs to confirm Rules, Actions and TargetGroups reflect the Ingress annotation weights, protecting against AWS rate limiting or controller downtime.

Enable by adding the flag to the controller arguments:

```yaml
args: [--aws-verify-target-group]
```

In v1.0 the flag was `--alb-verify-weight`. The `--aws-region` flag is mandatory for AWS integrations, and the pod needs Elastic Load Balancing API read permissions granted by access keys, kiam, kube2iam or an EKS service account IAM role.

Verify the flag appears in the controller Deployment args.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/traffic-management/alb/.

Removed or corrected: the claim that IP verification covers stableService IPs for canary; the controller-log verification step.

Method: documentation only; no commands were run.
