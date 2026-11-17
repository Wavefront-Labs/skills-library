---
id: computing-software.devops-ci-cd.spinnaker.aws-ec2-iam-setup
name: aws-ec2-iam-setup
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [aws, ec2, iam, managing-account, managed-account, assume-role, clouddriver]
level: practitioner
status: docs-checked
description: "Set up the AWS EC2 provider IAM: a spinnaker role assuming a spinnakerManaged role per target account, plus the clouddriver aws account block and Orca bake account."
sources:
  - https://spinnaker.io/docs/setup/install/providers/aws/aws-ec2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The AWS EC2 provider deploys EC2 resources; the most common use is baking AMIs, deploying them to new autoscaling groups and deleting the previous ones. The page recommends node or pod roles to access AWS securely, and IAM roles over IAM users (a user with access keys works but is not recommended).

**Model.** A Spinnaker Account maps to a credential for one AWS account. The page's example: Spinnaker runs in account `spinnaker` and assumes the `spinnakerManaged` role in the `develop` and `staging` accounts. Start by tabulating account names against account IDs.

**Two roles:**
- `spinnaker`: the role Spinnaker operates as. Trust relationship is EC2 (Spinnaker runs on the nodes holding the role; the page points to pod identity or IRSA for advanced setups). Its policy allows `ec2:DescribeAvailabilityZones` and `ec2:DescribeRegions` (for listing regions at startup) and `sts:AssumeRole`, which lets it assume into any target account (enabling dynamic account setup). Add further permissions, such as S3, depending on enabled features.
- `spinnakerManaged`, created in each target account with a custom trust policy whose principal is the `spinnaker` role in the Spinnaker account and action `sts:AssumeRole`. Attach the `PowerUserAccess` policy (more scoped permissions can be set) and an inline policy allowing `iam:ListServerCertificates` and `iam:PassRole`, which PowerUserAccess does not include; the page names it "PassRole-and-Certificates".

**Baking.** If Spinnaker creates AMIs, extra Packer permissions are needed; the page says they can be assigned to rosco through service accounts and IRSA to narrow scope, and gives an example policy.

**Clouddriver config:**

```yaml
aws:
  enabled: true
  primaryAccount: develop
  accounts:
  - name: develop
    environment: something
    defaultKeyPair: keypairs
    permissions:
      READ:
      - groupone
      WRITE:
      - groupone
    assumeRole: role/spinnakerManaged
    accountId: <ACCOUNT_ID>
    regions:
    - us-east-1
    - us-west-2
```

**Orca config:** set `default.bake.account` to one of the configured accounts.

The page recommends enabling AWS Launch Templates for autoscaling groups (it links a Launch Template Setup Guide).

## Checked

2026-11-04. Rewritten against the current Amazon EC2 page. Removed: the CloudFormation options 1 and 2 and the out-of-date banner (no longer on the page, which now documents the IAM console approach and clouddriver YAML).

Method: documentation only; no commands were run.
