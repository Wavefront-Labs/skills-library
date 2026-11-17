---
id: computing-software.cloud-infrastructure-engineering.aws.ami-id-lookup-via-ssm-parameters
name: ami-id-lookup-via-ssm-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ami, ssm-parameter-ami, latest-ami, ami-lookup, parameter-store, launch-template, image-builder]
level: practitioner
status: docs-checked
description: "Resolve AMI IDs through SSM parameters: AWS public parameters for the latest OS images, publishing your own golden AMI parameter, and launch templates that resolve it."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-public-parameters-ami.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-systems-manager-parameter-to-find-AMI.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-ec2-aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMI lookup via SSM parameters

**Goal:** stop hard-coding region-specific AMI IDs; every account and region resolves "the
current approved image" by name.

## 1. AWS public parameters
```bash
aws ssm get-parameter --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64 --query Parameter.Value --output text
aws ssm get-parameters-by-path --path /aws/service/ami-windows-latest --query 'Parameters[].Name'
```
Other public parameter trees (EKS-optimized, Bottlerocket) are listed in their own service guides.
Use directly at launch (resolved at launch time):
```bash
aws ec2 run-instances --image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 ...
```
The `resolve:ssm:<parameter-name>` form also takes a version: `resolve:ssm:<parameter-name>:<version>`.

## 2. Publish your golden AMI
After your image pipeline finishes, write the ID to a parameter:
```bash
aws ssm put-parameter --name /golden/al2023/web --type String --data-type aws:ec2:image \
  --value ami-0abc123 --overwrite
```
`--data-type aws:ec2:image` makes Parameter Store validate, on create or update, that the value is
in AMI ID format (the caller needs `ssm:GetParameters` permission for the validation to succeed).
Replicate the parameter per account in the pipeline.

## 3. Launch templates that follow the parameter
```bash
aws ec2 create-launch-template-version --launch-template-name web \
  --launch-template-data '{"ImageId":"resolve:ssm:/golden/al2023/web"}'
```
Each launch resolves the current value, so existing instances keep their old AMI until replaced.

## Gotchas
- "Latest" drifts: for reproducible prod, pin a parameter *version* (`/golden/al2023/web:12`)
  or have the pipeline update the parameter only after tests pass.
- Old AMIs that are deregistered break rollbacks to older parameter versions.

## Verify
- [ ] `aws ec2 describe-images --image-ids $(aws ssm get-parameter --name /golden/al2023/web --query Parameter.Value --output text)` returns the image.
- [ ] New ASG instances run the AMI the parameter points to (`describe-instances` ImageId).
- [ ] No hard-coded `ami-` IDs remain in IaC (`grep -R "ami-[0-9a-f]\{8,\}"`).

## Checked

2026-10-28. Confirmed against the EC2 "use a Systems Manager parameter to find an AMI" page, the Parameter Store public AMI parameters page and the EC2 aliases page: `resolve:ssm:<name>` and `resolve:ssm:<name>:<version>` syntax, aws:ec2:image data type validating AMI ID format, the al2023-ami-kernel-default-* and ami-windows-latest parameter paths. Removed (unconfirmed): Bottlerocket and EKS parameter paths, CloudFormation and CDK mechanics, Image Builder and RAM claims, 100-version retention, instance refresh advice, and the claim that validation checks the AMI exists (the page says format). Read end to end.

Method: documentation only; no commands were run.
