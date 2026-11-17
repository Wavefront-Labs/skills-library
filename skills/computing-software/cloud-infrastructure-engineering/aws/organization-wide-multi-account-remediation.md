---
id: computing-software.cloud-infrastructure-engineering.aws.organization-wide-multi-account-remediation
name: organization-wide-multi-account-remediation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, multi-account-remediation, aws-config, conformance-packs, ssm-automation, security-hub-automation, organizations, delegated-administrator]
level: practitioner
status: docs-checked
description: "Run remediation across every account: AWS Config organization conformance packs with remediation actions, delegated administrator deployment, and rollout safety."
sources:
  - https://docs.aws.amazon.com/config/latest/developerguide/conformance-packs.html
  - https://docs.aws.amazon.com/config/latest/developerguide/conformance-pack-deploy.html
  - https://docs.aws.amazon.com/config/latest/developerguide/config-rule-multi-account-deployment.html
  - https://docs.aws.amazon.com/config/latest/developerguide/setup-autoremediation.html
  - https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-v2-automation-rules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organization-wide remediation across accounts

## Building blocks
| Need | Mechanism |
|---|---|
| Same rules and fixes in every account | AWS Config **organizational conformance pack**: a collection of Config rules and remediation actions deployed across an organization |
| Same single rule everywhere | AWS Config organizational rule |
| Central handling of findings | Security Hub automation rules |

## Deploy from the right account
- Deploy organizational rules and conformance packs from the organization management account or a Config **delegated administrator**. Deploying from both accounts has overlap rules: read the multi-account deployment page before mixing them.
- A conformance pack template can include remediation actions; the deployment page links the prerequisites for using a conformance pack with remediation.
- Remediation applies only to non-service-linked Config rules.
- The SSM Automation assume role used by a remediation must exist in every member account before the pack is deployed (roll it out first, for example with a service-managed StackSet).

```bash
aws configservice put-organization-conformance-pack --organization-conformance-pack-name <PACK_NAME> \
  --template-body file://<TEMPLATE_FILE> --excluded-accounts <ACCOUNT_ID>
```

## Safety
Start in report-only, roll out by OU (sandbox, dev, prod), exclude break-glass accounts, and notify owners of every automatic change.

## Verify
- [ ] `aws configservice describe-organization-conformance-pack-statuses` shows the pack created in all accounts.
- [ ] A non-compliant test resource in a member account is fixed and the action is logged centrally.

## Checked
2026-10-28. Confirmed on the AWS Config pages "Conformance Packs", "Deploying Conformance Packs", "Organizational Rules" and "Setting Up Auto Remediation", and the Security Hub automation rules page: organizational conformance packs as collections of rules and remediation actions across an organization, management and delegated administrator deployment, remediation limited to non-service-linked rules; `check_commands.py` accepted both Config CLI commands.
Removed as unconfirmed: the CloudFormation `RemediationConfiguration` example, the multi-account SSM Automation command and its role names, the Security Hub to EventBridge to Lambda flow and custom actions, Firewall Manager, and the `CREATE_SUCCESSFUL` status value.
Method: documentation only; no commands were run.
