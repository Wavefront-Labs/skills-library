---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-unreachable-instance-troubleshooting
name: ec2-unreachable-instance-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, status-checks, instance-console-output, ec2-serial-console, rescue-volume, boot-failure, troubleshooting]
level: practitioner
status: docs-checked
description: "Recover an EC2 instance that will not boot or answer: status checks, console output and screenshot, EC2 Serial Console, and the rescue-volume procedure."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-serial-console.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-serial-console-prerequisites.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-to-serial-console.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-configuration-recovery.html", "https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-awssupport-executeec2rescue.html", "https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-awssupport-resetaccess.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting an unreachable EC2 instance

## 1. Status checks tell you whose problem it is
```bash
aws ec2 describe-instance-status --instance-ids i-123 --include-all-instances \
  --query 'InstanceStatuses[0].[SystemStatus.Status,InstanceStatus.Status,AttachedEbsStatus.Status]'
```
- **System status impaired** → problem with the underlying host: stop and start the instance (in most cases this migrates it to a new host), or rely on
  simplified automatic recovery or a `StatusCheckFailed_System` alarm with the recover action.
- **Instance status impaired** → your OS: kernel panic, bad fstab, full disk, network config.
- **Attached EBS status impaired** → an attached volume has I/O problems (Nitro instances only).

## 2. Look at the screen
```bash
aws ec2 get-console-output --instance-id i-123 --latest --output text | tail -80
aws ec2 get-console-screenshot --instance-id i-123 --query ImageData --output text | base64 -d > shot.jpg
```
Look for kernel panics, emergency-mode prompts caused by fstab, cloud-init errors, or Windows boot messages.

## 3. EC2 Serial Console (interactive, no network needed)
```bash
aws ec2 enable-serial-console-access              # account/region level, once
aws ec2-instance-connect send-serial-console-ssh-public-key --instance-id i-123 --serial-port 0 --ssh-public-key file://key.pub
ssh -i key i-123.port0@serial-console.ec2-instance-connect.<REGION>.aws
```
Needs an instance built on the Nitro System. To troubleshoot a Linux instance you need a password-based OS user (AWS AMIs have none by default, so set one beforehand with `passwd`)
and GRUB or SysRq configured for the serial console. Only one session per instance at a time; ssh within 60 seconds of sending the key.
Restrict with IAM (`ec2-instance-connect:SendSerialConsoleSSHPublicKey`) and grant account access with `enable-serial-console-access`.

## 4. Rescue volume procedure (last resort)
1. Stop the instance (snapshot the root volume first).
2. Detach the root volume; attach to a helper instance in the **same AZ** as `/dev/sdf`.
3. Mount the root partition, for example `sudo mount /dev/nvme1n1p1 /mnt/rescue`.
4. Fix: `/mnt/rescue/etc/fstab` (add `nofail`), the login user's `.ssh/authorized_keys` under `/mnt/rescue` (e.g. `<OS_USER_HOME>/.ssh/authorized_keys`),
   `/mnt/rescue/etc/ssh/sshd_config`, free disk space.
5. Unmount, detach, reattach as the instance's original root device name (see `RootDeviceName` in `describe-instances`), start.
Automation: the SSM runbooks `AWSSupport-ExecuteEC2Rescue` (troubleshoots and repairs common connectivity issues with the EC2Rescue tool) and `AWSSupport-ResetAccess` (resets SSH keys or Windows password access) cover common cases; ExecuteEC2Rescue does not support instances with encrypted root volumes.

## Gotchas
- Always add `nofail` to non-root fstab entries — a missing EBS volume shouldn't brick boot.

## Verify
- [ ] Both status checks `ok` after the fix; SSH/SSM connects.
- [ ] `StatusCheckFailed_System` alarm with recover action exists for single-instance workloads.
- [ ] Serial console access enabled (and IAM-restricted) in accounts where break-glass is needed.

## Checked

Checked 2026-10-27 against the Amazon EC2 User Guide (status checks, automatic instance recovery, EC2 Serial Console prerequisites, access configuration and connect pages), the Systems Manager Automation runbook reference and the botocore EC2 model.
- Status check types, `StatusCheckFailed_System` recovery, stop and start usually moving the instance, and the attached EBS check being Nitro-only confirmed on the status checks page.
- Serial console: Nitro requirement, password-based OS user and GRUB or SysRq setup for Linux, `enable-serial-console-access`, `send-serial-console-ssh-public-key`, `instance-id.port0` user, one session at a time and the 60-second window confirmed.
- `AWSSupport-ExecuteEC2Rescue` and `AWSSupport-ResetAccess` descriptions confirmed; ExecuteEC2Rescue does not support encrypted root volumes. `get-console-output --latest`, `get-console-screenshot` and `describe-instance-status --include-all-instances` confirmed in the service model.
- Removed the XFS `nouuid` tip, the instance-store remark and the quoted console messages, which no page read confirms.

Method: documentation only; no commands were run.
