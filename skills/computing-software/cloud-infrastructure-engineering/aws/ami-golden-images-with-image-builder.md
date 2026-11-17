---
id: computing-software.cloud-infrastructure-engineering.aws.ami-golden-images-with-image-builder
name: ami-golden-images-with-image-builder
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ami, image-builder, ec2-image-builder, golden-image, golden-ami, image-pipeline, image-recipe, ami-lifecycle, ami-sharing, ami-deprecation, ssm-parameter, launch-template, packer, cis-hardening, ami-distribution, create-image, copy-image, encrypted-ami, kms]
level: practitioner
status: draft
description: "Build, test, distribute and retire golden AMIs with EC2 Image Builder: recipes, components, pipelines, SSM-parameter publishing, cross-account sharing and AMI deprecation."
sources: ["https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html", "https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-components.html", "https://docs.aws.amazon.com/AWSEC2/LatestUserGuide/AMIs.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ami-deprecate.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sharingamis-explicit.html", "https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-image-recipes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Golden AMIs with EC2 Image Builder

**Goal:** a repeatable pipeline that bakes a hardened, patched AMI on a schedule, tests
it, copies/shares it to every account and region that needs it, publishes its id to an
SSM parameter that launch templates resolve, and deprecates old AMIs so nothing stale
launches.

## 1. Why bake instead of bootstrap
User-data installs make scale-out slow (minutes) and non-deterministic (upstream repo
changed). Bake everything that does not change per instance (agents, runtime, hardening);
leave only config injection to user data (see
`computing-software.cloud-infrastructure-engineering.aws.ec2-autoscaling`).

## 2. Image Builder building blocks
| Object | What it is |
|---|---|
| **Component** | YAML document (AWSTOE) with `build`, `validate`, `test` phases of steps (`ExecuteBash`, `ExecutePowerShell`, `S3Download`, `Reboot`…) |
| **Image recipe** | Parent image + ordered components + block device mapping (+ optional `workingDirectory`) |
| **Infrastructure config** | Instance type(s), subnet, SG, instance profile, logging bucket, `terminateInstanceOnFailure` |
| **Distribution config** | Target regions/accounts, AMI name pattern, launch-template update, SSM parameter to publish |
| **Pipeline** | Recipe + infra + distribution + schedule (cron) + image tests enabled |

Parent image: use the AWS-managed ARN with `x.x.x` so the pipeline always picks the
latest patched base, e.g.
`arn:aws:imagebuilder:us-east-1:aws:image/amazon-linux-2023-x86-64/x.x.x`.

Minimal component:
```yaml
name: install-cw-agent
schemaVersion: 1.0
phases:
  - name: build
    steps:
      - name: Install
        action: ExecuteBash
        inputs:
          commands:
            - dnf install -y amazon-cloudwatch-agent
  - name: validate
    steps:
      - name: Check
        action: ExecuteBash
        inputs:
          commands:
            - test -x /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent
  - name: test
    steps:
      - name: Running
        action: ExecuteBash
        inputs:
          commands:
            - systemctl is-enabled amazon-cloudwatch-agent
```
`build`/`validate` run on the build instance; `test` runs on a fresh instance launched
from the candidate AMI (only when the pipeline has image tests enabled). Use AWS-managed
components for the boring parts: `update-linux`, `amazon-cloudwatch-agent-linux`,
`stig-build-linux-high`, `aws-cli-version-2-linux`.

## 3. Instance profile for the build instance
Attach `EC2InstanceProfileForImageBuilder` + `AmazonSSMManagedInstanceCore` (AWSTOE is
delivered over SSM). Add `EC2InstanceProfileForImageBuilderECRContainerBuilds` only for
container recipes. Build subnet needs outbound to SSM/S3/package repos (NAT or endpoints).

## 4. Distribution: publish to SSM and share
Distribution config can, per region:
- copy the AMI (`amiDistributionConfiguration`: `name: "app-{{ imagebuilder:buildDate }}"`,
  `launchPermission.userIds` for account sharing, `targetAccountIds` to copy into accounts
  rather than share);
- update a launch template's default version (`launchTemplateConfigurations`);
- write the AMI id to an SSM parameter (`ssmParameterConfigurations`, parameter
  `/golden/ami/app`), which launch templates reference as `resolve:ssm:/golden/ami/app`.

Encrypted AMIs: sharing an AMI backed by a KMS-encrypted snapshot requires the target
account to have `kms:DescribeKey`, `kms:ReEncrypt*`, `kms:CreateGrant`, `kms:Decrypt` on
the customer-managed key — AWS-managed `aws/ebs` keys cannot be shared, so always use
a CMK for golden images. Prefer **copying into** the target account (`targetAccountIds`)
over sharing when the consumer must own the AMI (e.g. for their own deprecation policy).

## 5. Manual AMI operations you still need
```bash
# Ad-hoc image from a configured instance (reboot=true for filesystem consistency)
aws ec2 create-image --instance-id i-0abc --name "app-manual-$(date +%F)" --reboot
# Copy cross-region with re-encryption
aws ec2 copy-image --source-region us-east-1 --source-image-id ami-0abc \
  --region eu-west-1 --name app-eu --encrypted --kms-key-id alias/ebs-golden
# Share
aws ec2 modify-image-attribute --image-id ami-0abc --launch-permission "Add=[{UserId=<ACCOUNT_ID>}]"
# Retire
aws ec2 enable-image-deprecation --image-id ami-0abc --deprecate-at 2026-12-31T00:00:00Z
aws ec2 deregister-image --image-id ami-0abc   # then delete its snapshots yourself
```
Deprecation hides the AMI from unfiltered `describe-images` and from console/launch
template pickers, but **existing launch templates and ASGs still launch it** — rotate the
SSM parameter first, then deprecate. Deregister removes the AMI; the EBS snapshots stay
and keep billing until `delete-snapshot`. Image Builder **lifecycle policies** can
automate deprecate → disable → deregister + snapshot deletion by age or count.

## 6. Pipeline hygiene
- Schedule with `pipelineExecutionStartCondition: EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE`
  so a cron tick only builds when the parent image or a component actually changed.
- Enable **enhanced image metadata** and **image scanning** (Inspector) in the pipeline;
  fail the pipeline on critical CVEs via an EventBridge rule on `EC2 Image Builder Image State Change`.
- Version components semantically; recipes pin component versions (or `x.x.x` for latest).
- Keep `terminateInstanceOnFailure: false` while debugging a component; otherwise you
  lose the build instance before you can read `/var/lib/amazon/toe/` logs. Logs also
  land in the configured S3 bucket under `<pipeline>/<version>/<build>/`.

## Gotchas
- A recipe's block device mapping overrides the parent's; forgetting to set root volume
  size inherits the base (8 GiB on AL2023) and the first `dnf` run fills it.
- Windows: Sysprep is run by the managed `windows-sysprep`-equivalent step; a custom
  reboot step after sysprep-like actions breaks the image. Use the `Reboot` action, not
  `shutdown /r` in a script.
- AWSTOE `ExecuteBash` runs as root with no login shell; `$HOME` and PATH differ from an
  interactive session. Use absolute paths.
- Cross-region distribution is a **copy**; the AMI ids differ per region — always resolve
  via SSM parameter per region, never hard-code ids in templates.
- `describe-images --owners self` lists deprecated images only with `--include-deprecated`.
- Unconfirmed: exact Inspector scanning regional availability for Image Builder; check the
  current region table.

## Verify
- [ ] Pipeline run ends `AVAILABLE`, image tests pass, Inspector findings reviewed.
- [ ] `aws ssm get-parameter --name /golden/ami/app` returns the new AMI id in every target region.
- [ ] A fresh launch from the launch template boots to healthy without user-data package installs.
- [ ] Old AMIs show `DeprecationTime` set and no ASG launch template resolves to them.
- [ ] Orphan snapshots: `describe-snapshots --owner-ids self` has none whose description references a deregistered AMI.
