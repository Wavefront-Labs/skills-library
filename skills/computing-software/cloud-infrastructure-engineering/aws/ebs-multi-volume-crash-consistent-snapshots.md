---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-multi-volume-crash-consistent-snapshots
name: ebs-multi-volume-crash-consistent-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, multi-volume-snapshot, crash-consistent, application-consistent, data-lifecycle-manager]
level: advanced
status: docs-checked
description: "Take crash-consistent multi-volume EBS snapshots of an instance, add application consistency with VSS or fsfreeze scripts, and automate with Data Lifecycle Manager."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/ebs-create-snapshots.html", "https://docs.aws.amazon.com/ebs/latest/userguide/automate-app-consistent-backups.html", "https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html", "https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/application-consistent-snapshots.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crash-consistent and multi-volume snapshots

## 1. Consistency levels
| Level | How | Good for |
|---|---|---|
| Crash-consistent, single volume | `create-snapshot` | single-disk apps with journaling |
| Multi-volume snapshot set | `create-snapshots` (all attached volumes in one request, up to 128 volumes) | RAID sets, DB data + log on separate volumes |
| Application-consistent | quiesce app/filesystem around the snapshot | databases without their own backup tooling |

## 2. Multi-volume snapshot
```bash
aws ec2 create-snapshots --instance-specification InstanceId=i-0abc,ExcludeBootVolume=true \
  --copy-tags-from-source volume --description "db pre-upgrade" \
  --tag-specifications 'ResourceType=snapshot,Tags=[{Key=set,Value=db-2026-10-18}]'
```
The set is one operation: if any snapshot fails, the others enter the `error` state and a
`createSnapshots` event with result `failed` is sent (`succeeded` otherwise). Each snapshot is an
ordinary snapshot, and you can also exclude data volumes with `ExcludeDataVolumeIds`. Restore the
volumes **together** as a set. The limit is 128 attached volumes (root plus 127 data volumes).

## 3. Application consistency
- Linux: `fsfreeze -f /data`, snapshot, `fsfreeze -u /data` (the AWS sample pre and post scripts use these commands).
- Windows: VSS via the SSM Run Command document `AWSEC2-VssInstallAndSnapshot`, which needs the `AwsVssComponents` Distributor package and instance permissions. VSS pauses I/O for at most ten seconds, and the snapshots it creates are tagged `AppConsistent:true`.
- DLM: policies support pre and post scripts run through SSM (`Scripts` in the policy schedule) for
  freeze/thaw or VSS (`ExecutionHandler: AWS_VSS_BACKUP`); `ExecutionTimeout` is 10 to 120 seconds and `MaximumRetryCount` 0 to 3. If the pre script fails you can default to crash-consistent snapshots or create none. Target instances need the tag `DLMScriptsAccess:true` for the managed SSM permissions.

## 4. Automate with DLM
An EBS snapshot policy with `ResourceTypes: ["INSTANCE"]` and target tags takes multi-volume snapshots on schedule with retention.

## Verify
- [ ] Restore the full snapshot set to a test instance; filesystem mounts cleanly and DB recovery succeeds.

## Checked

Checked 2026-10-27 against the Amazon EBS User Guide (Create multi-volume snapshots, Automate application-consistent snapshots, Data Lifecycle Manager elements), the Amazon EC2 Windows guide (VSS based snapshots) and the botocore EC2 model.
- `create-snapshots` options (`InstanceSpecification` with `ExcludeBootVolume` and `ExcludeDataVolumeIds`, `CopyTagsFromSource=volume`, tag specifications), the failure behaviour and the 128-volume limit confirmed.
- The Windows SSM document name was wrong (`AWSEC2-CreateVssSnapshot`); the documented one is `AWSEC2-VssInstallAndSnapshot`.
- DLM `Scripts` fields, handler names, timeout and retry ranges, the crash-consistent fallback and the policy `ResourceTypes` list form confirmed.
- Removed the "same instant" capture claim, the MySQL lock remark and cross-Region copy for instance policies, which the pages read did not confirm.

Method: documentation only; no commands were run.
