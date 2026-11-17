---
id: computing-software.cloud-infrastructure-engineering.aws.control-tower-customizations-cfct-and-lza
name: control-tower-customizations-cfct-and-lza
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, control-tower, cfct, landing-zone-accelerator, manifest-yaml, stacksets, landing-zone, account-baseline]
level: advanced
status: draft
description: "Baseline every Control Tower account with Customizations for Control Tower (manifest.yaml, SCPs and StackSets via pipeline) or Landing Zone Accelerator config files."
sources: ["https://docs.aws.amazon.com/controltower/latest/userguide/cfct-overview.html", "https://docs.aws.amazon.com/controltower/latest/userguide/cfcn-byo-customizations.html", "https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/solution-overview.html", "https://github.com/aws-solutions/aws-control-tower-customizations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control Tower customizations: CfCT and Landing Zone Accelerator

**Goal:** every account Control Tower enrolls or vends receives the organisation's
baseline (extra SCPs, IAM roles, VPC, logging, security config) automatically and
reproducibly from Git.

## 1. Pick the tool
| | CfCT | Landing Zone Accelerator (LZA) |
|---|---|---|
| Model | Your CloudFormation templates + SCP JSON, deployed per a `manifest.yaml` | Opinionated YAML config (`accounts-config.yaml`, `network-config.yaml`, `security-config.yaml`...) driving CDK |
| Scope | Thin: "run these stacks/SCPs on these OUs/accounts" | Broad: networking (TGW, inspection, endpoints), security services, logging, IAM, compliance baselines (e.g. TSE, CCCS, NIST) |
| Fit | Teams that already write CFN and want control | Regulated/greenfield wanting a full reference architecture |
| Trigger | Control Tower lifecycle event `CreateManagedAccount` + pipeline run | Pipeline run and lifecycle events |
Control Tower Account Factory for Terraform (AFT) is the Terraform-world equivalent.

## 2. CfCT
Deploy the solution's CloudFormation template in the management account (home region).
It creates a CodePipeline sourced from S3 or CodeCommit/CodeConnections.

Repository layout:
```
manifest.yaml
policies/deny-leave-org.json
templates/baseline-roles.yaml
parameters/baseline-roles.json
```
`manifest.yaml` (version 2021-03-15):
```yaml
region: eu-west-1
version: 2021-03-15
resources:
  - name: deny-leave-org
    resource_file: policies/deny-leave-org.json
    deploy_method: scp
    deployment_targets:
      organizational_units: [Workloads, Sandbox]
  - name: baseline-roles
    resource_file: templates/baseline-roles.yaml
    parameter_file: parameters/baseline-roles.json
    deploy_method: stack_set
    deployment_targets:
      organizational_units: [Workloads, Sandbox, Security]
    regions: [eu-west-1, eu-central-1]
    export_outputs:
      - name: /org/baseline/role-arn
        value: $[output_RoleArn]
```
- `deploy_method: scp` or `rcp` attaches policies; `stack_set` creates StackSet instances.
- Targets by OU name (nested OUs as `Root:Workloads:Prod` path syntax) or account name/ID.
- Parameter values can pull `$[alfred_ssm_/path]` from SSM in the management account.
- Pipeline stages: build (validates manifest and templates with cfn-nag/cfn-lint),
  SCP stage, StackSet stage. A failed stack in one account fails the pipeline run;
  fix and rerun.
- New account vended by Account Factory triggers the pipeline via the lifecycle event,
  so baselines land within minutes of enrollment.

## 3. LZA
Deployed from the solution template; config lives in a CodeCommit/S3/GitHub repo:
- `organization-config.yaml` OUs, SCPs, tag/backup policies.
- `accounts-config.yaml` mandatory accounts and workload accounts (email, OU).
- `network-config.yaml` TGW, VPCs, IPAM, endpoints, Network Firewall.
- `security-config.yaml` GuardDuty, Security Hub standards, Macie, Config rules.
- `iam-config.yaml` roles, policies, Identity Center assignments.
- `global-config.yaml` home region, enabled regions, logging, Control Tower settings.
Changes go through the LZA pipeline (Build, Prepare, Accounts, Bootstrap, Deploy
stages). Use `customizations-config.yaml` for your own CFN/StackSets.

## 4. Operating either
- Treat the repo as the only change path: protect the branch, require review.
- Upgrade the solution itself on its release cadence (new template version); read the
  release notes for breaking config changes.
- Control Tower landing zone updates: run CfCT/LZA after, since CT may reset controls.
- Drift: StackSet drift detection on baseline stacks; CT drift for SCPs CT manages.

## Gotchas
- CfCT SCP names must not collide with Control Tower's `aws-guardrails-*` policies, and
  the 5-SCP-per-target limit includes CT's own.
- StackSets via CfCT run as `AWSControlTowerExecution`; templates needing org-level
  permissions fail in member accounts.
- LZA creates many resources (TGW, firewalls) that cost money on day one; review
  `network-config.yaml` defaults before the first run.

## Verify
- [ ] Vending a test account via Account Factory results in baseline stacks and SCPs within one pipeline run, with no manual steps.
- [ ] Pipeline history green on last run; failures alert to the platform channel.
- [ ] Removing a baseline role manually in a test account is detected by drift and restored on the next run.
