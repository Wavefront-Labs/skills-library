---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-stop-hibernate-and-instance-lifecycle
name: ec2-stop-hibernate-and-instance-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, instance-lifecycle, stop-start, hibernate, termination-protection, instance-store, scheduled-events]
level: practitioner
status: docs-checked
description: "Manage EC2 instance lifecycle: what survives stop, hibernate, reboot and terminate; enabling hibernation; termination/stop protection; and handling scheduled retirement events."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/hibernating-prerequisites.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-hibernate-overview.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-instances-status-check_sched.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_ChangingDisableAPITermination.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 stop, hibernate and lifecycle

## 1. What survives what
| | Reboot | Stop | Hibernate | Terminate |
|---|---|---|---|---|
| Underlying host | same | usually new | usually new | — |
| Instance store data | kept | **lost** | **lost** | lost |
| EBS root/data | kept | kept | kept (RAM saved to root) | deleted if `DeleteOnTermination` |
| RAM contents | lost | lost | **restored** | — |
| Private IPv4 / ENI | kept | kept | kept | released |
| Auto-assigned public IP | kept | **changes** | **changes** | released (EIP stays allocated) |
| Billing | continues | instance usage stops once `stopped` (EBS still billed) | billed while `stopping`, not once `stopped`; RAM data storage on EBS is billed | stops |

## 2. Hibernation
Must be enabled **at launch** with an encrypted root EBS volume large enough for RAM + OS:
```bash
aws ec2 run-instances --image-id ami-123 --instance-type m7i.large \
  --hibernation-options Configured=true \
  --block-device-mappings 'DeviceName=/dev/xvda,Ebs={VolumeSize=40,Encrypted=true}'
aws ec2 stop-instances --instance-ids i-123 --hibernate
```
Limits: it cannot be enabled on an existing instance; Linux RAM must be under 150 GiB (Windows 16 GiB or less);
no more than 60 days hibernated; supported AMIs and instance families only (bare metal excluded); root volume must be
encrypted EBS (gp2, gp3, io1 or io2); not for instances in an Auto Scaling group or used by Amazon ECS, nor UEFI Secure
Boot instances. Instance store data is lost and, while hibernated, the instance cannot be modified. Use for long-warmup
apps (JVM caches, dev boxes).

## 3. Protection
```bash
aws ec2 modify-instance-attribute --instance-id i-123 --disable-api-termination
aws ec2 modify-instance-attribute --instance-id i-123 --disable-api-stop
aws ec2 modify-instance-attribute --instance-id i-123 --instance-initiated-shutdown-behavior stop
```
Termination and stop protection do not protect against stops or terminations started from inside the operating system
(for example `shutdown`); the shutdown-behaviour attribute (default `stop` for EBS-backed instances) controls the result.

## 4. Scheduled events
AWS schedules `instance-retirement`, `system-reboot`, `instance-stop` for degraded hardware:
```bash
aws ec2 describe-instance-status --filters Name=event.code,Values=instance-retirement,instance-stop,system-reboot \
  --query 'InstanceStatuses[].[InstanceId,Events[0].Code,Events[0].NotBefore]'
```
Act early: stop/start (EBS-backed) moves to healthy hardware. Subscribe to AWS Health events
in EventBridge to automate. `aws ec2 modify-instance-event-start-time` reschedules some events.

## Gotchas
- Instance store "ephemeral" disks used as caches must be re-initialised on every start.
- Stopping an instance with an auto-assigned public IP breaks anything that hard-coded it — use an EIP or DNS.
- Stopped instances still incur charges for EBS volumes and Elastic IP addresses, which are billed regardless of instance state.

## Verify
- [ ] Hibernate test: process state (e.g. an open `tmux` session) survives `stop --hibernate` and start.
- [ ] Production instances have termination (and where appropriate stop) protection enabled.
- [ ] EventBridge rule routes `AWS Health` scheduled-change events for EC2 to the on-call channel.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide pages "Amazon EC2 instance state changes", "Prerequisites for EC2 instance hibernation", "How Amazon EC2 instance hibernation works" and "Scheduled events for Amazon EC2 instances"; botocore EC2 model (RunInstances HibernationOptions.Configured, StopInstances Hibernate, ModifyInstanceAttribute DisableApiTermination/DisableApiStop/InstanceInitiatedShutdownBehavior, ModifyInstanceEventStartTime).
Corrected: hibernation is billed while the instance is in the stopping state (the skill said "same as stop"); Linux RAM limit is below 150 GiB and Windows is 16 GiB or less; hibernation cannot be enabled after launch and is not supported in Auto Scaling groups.
Confirmed: reboot, stop, hibernate and terminate behaviour for host, private IP, public IP, EIP, IPv6, instance store, root volume and RAM; 60-day hibernation limit; event codes instance-retirement, instance-stop, system-reboot.
Removed: the ec2-hibinit-agent detail, the Auto Scaling scale-in remark and the public IPv4 hourly-billing statement (pricing is not checked here).

Method: documentation only; no commands were run.
