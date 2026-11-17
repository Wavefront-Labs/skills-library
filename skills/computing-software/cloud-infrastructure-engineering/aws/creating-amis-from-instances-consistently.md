---
id: computing-software.cloud-infrastructure-engineering.aws.creating-amis-from-instances-consistently
name: creating-amis-from-instances-consistently
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ami, no-reboot, create-image, ebs-snapshots, register-image]
level: practitioner
status: docs-checked
description: "Create an EBS-backed AMI from a running instance: reboot vs no-reboot, tags on image and snapshots, block device mappings, encryption, snapshot cost and creating from a snapshot."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating AMIs from instances

For repeatable golden images use a build pipeline such as EC2 Image Builder; this skill is for capturing an existing
EBS-backed instance (the console's Create image is disabled for instances that are not EBS-backed).

## 1. Reboot vs no-reboot
```bash
aws ec2 create-image --instance-id <INSTANCE_ID> --name "<NAME>" --description "<DESCRIPTION>" \
  --no-reboot \
  --tag-specifications 'ResourceType=image,Tags=[{Key=purpose,Value=pre-upgrade}]' \
                       'ResourceType=snapshot,Tags=[{Key=purpose,Value=pre-upgrade}]'
```
- Default: Amazon EC2 powers the instance down before creating the AMI so everything is stopped and consistent
  (console: the "Reboot instance" checkbox is selected by default).
- With `--no-reboot` (console: clear Reboot instance) the instance keeps running. The page warns that AWS cannot
  guarantee the file system integrity of the created image. Use it only if you are confident the instance is in a
  consistent state; the page notes that file systems such as XFS can freeze and unfreeze activity, which makes
  creating the image without a reboot safe.
- The API model gives `Name` as 3-128 characters (the console page says up to 127) and `Description` up to 255.

## 2. What is captured
- EC2 snapshots the root volume and every other attached EBS volume. You are charged for those snapshots until you
  deregister the AMI **and** delete the snapshots.
- If any attached volume is encrypted, the new AMI launches only on instance types that support EBS encryption.
- Instance store volumes in the new AMI's block device mapping come up new, without data from the source instance's
  instance store volumes. Extra EBS volumes you added are attached automatically at launch; empty ones need formatting
  and mounting.
- Creation can take several minutes and, per the page, sometimes up to 24 hours depending on volume size. Snapshotting
  the volumes first makes the AMI step quicker because only small incremental snapshots remain (total snapshot time is unchanged).
- After launching from an EBS-backed AMI, initialize the root and any additional EBS volumes before production use.

## 3. Block device mappings and tags
`--block-device-mappings` (model fields `DeviceName`, `Ebs`, `NoDevice`, `VirtualName`) changes volumes at creation;
the console lets you resize the root volume, set Delete on termination and add volumes.
- Tags: console options are to tag the image and snapshots together, or separately; with separate tags all snapshots
  still get the same tags. The CLI takes `--tag-specifications` with `ResourceType=image` and `snapshot`.
- In a Local Zone that supports EBS local snapshots you choose the snapshot destination (Region or Local Zone) and all
  the instance's snapshots must be in the same location or creation fails. `--snapshot-location` is the API field.
- `BootModeOverride` accepts `uefi`, and the page says it only works if the instance's boot mode is already UEFI.

## 4. Watch completion
```bash
aws ec2 wait image-available --image-ids <IMAGE_ID>
```
The AMI shows `pending` and should become `available`; the snapshot's Description contains the AMI ID.

## 5. From a snapshot instead
`aws ec2 register-image --name <NAME> --root-device-name /dev/xvda --block-device-mappings DeviceName=/dev/xvda,Ebs={SnapshotId=<SNAPSHOT_ID>}`.
For Windows, Red Hat, SUSE and SQL Server, check the new AMI's Platform details field; if it is empty or wrong, discard the
AMI and create it from the instance instead (licensing information is derived from the snapshot's metadata).

## Verify
- [ ] Image state is `available` and the snapshots carry the expected tags.
- [ ] An instance launched from it passes status checks and the application starts with intact data.

## Checked
Date: 2026-11-07. Read in full: "Create an Amazon EBS-backed AMI" (overview, create from instance for console/CLI,
create from snapshot). API model checked for `CreateImage` fields and limits. Removed because no page read states
them: `fsfreeze`/database-lock recipes, Windows VSS and `AWSEC2-CreateVssSnapshot`, AWS Backup pre/post scripts, the
`truncate machine-id` / `cloud-init clean` / Sysprep clean-up, the multi-volume point-in-time claim, hibernation and
LVM/RAID gotchas, and the secrets-scan verify step. Dropped two source URLs that returned empty pages
(ami-create-windows-ami, application-consistent-snapshots); the clean-up and consistency material they were meant to
back is therefore no longer in this skill.
Method: documentation only; no commands were run.
