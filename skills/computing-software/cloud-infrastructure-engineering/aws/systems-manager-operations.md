---
id: computing-software.cloud-infrastructure-engineering.aws.systems-manager-operations
name: systems-manager-operations
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, systems-manager, ssm, session-manager, run-command, patch-manager, state-manager, ssm-agent, ssm-documents, patch-baseline, maintenance-window, inventory, fleet-manager, port-forwarding, bastionless, quick-setup, hybrid-activations]
level: practitioner
status: draft
description: "Run fleets with Systems Manager: Session Manager instead of SSH/bastions (with logging and port forwarding), Run Command at scale, Patch Manager baselines and windows, State Manager associations."
sources: ["AWS Systems Manager User Guide - Session Manager", "AWS Systems Manager User Guide - Run Command", "AWS Systems Manager User Guide - Patch Manager", "AWS Systems Manager User Guide - State Manager"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Systems Manager — shell, commands, patches and config for every instance, no inbound ports

**Goal:** no SSH keys or bastions; every interactive session logged; commands and patches
applied by tag at controlled rates; configuration drift corrected automatically.

## 1. Prerequisites (where 90 % of "instance not managed" comes from)
- **SSM Agent** running (preinstalled on Amazon Linux, Ubuntu, Windows AMIs).
- Instance profile with `AmazonSSMManagedInstanceCore` (or **Default Host Management
  Configuration** at account level so no profile is needed).
- Outbound HTTPS to `ssm`, `ssmmessages`, `ec2messages` endpoints — via NAT or, for private
  subnets, three **interface VPC endpoints** (`com.amazonaws.<region>.ssm|ssmmessages|ec2messages`)
  with a security group allowing 443 from the instance SG.
- Check: `aws ssm describe-instance-information --query 'InstanceInformationList[].[InstanceId,PingStatus,AgentVersion]'`.
- On-prem/other-cloud machines: `create-activation` → install agent with the code → appear as `mi-…`.

## 2. Session Manager
```bash
aws ssm start-session --target i-0123456789abcdef0
aws ssm start-session --target i-… --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["db.internal"],"portNumber":["5432"],"localPortNumber":["15432"]}'
```
- Install the **session-manager-plugin** on the client. SSH over SSM:
  `ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters portNumber=%p"`.
- **Preferences** (`SSM-SessionManagerRunShell` document): log to S3 + CloudWatch Logs
  (session transcript), KMS-encrypt sessions, idle timeout, `runAsEnabled` with a non-root user,
  shell profile (`cd /; umask 077`).
- Lock down with IAM: `ssm:StartSession` on instance ARNs with tag conditions
  (`ssm:resourceTag/env`), and `ssm:SessionDocumentAccessCheck` so users must use the
  approved document. Then **delete inbound 22/3389** from security groups.

## 3. Run Command
```bash
aws ssm send-command --document-name AWS-RunShellScript \
  --targets Key=tag:role,Values=web \
  --parameters 'commands=["systemctl restart nginx"]' \
  --max-concurrency 10% --max-errors 1 \
  --output-s3-bucket-name ops-logs --cloud-watch-output-config CloudWatchOutputEnabled=true
aws ssm list-command-invocations --command-id <id> --details
```
- Target by tags or a **resource group**, not instance ids. Rate control
  (`max-concurrency`, `max-errors`) is your blast-radius limit.
- Write your own **Command documents** (`schemaVersion 2.2`, `aws:runShellScript` /
  `aws:runPowerShellScript` steps) with parameters; version them; share across accounts.
- Output over 2 500 chars is truncated in the console — send to S3/CloudWatch.

## 4. Patch Manager
- **Patch baseline** per OS: auto-approve rules (e.g. `Classification=Security,Critical`
  after 7 days), rejected patches list, compliance severity. Set it as default per OS or
  attach via the **patch group** tag (`Patch Group=prod-linux`).
- Run `AWS-RunPatchBaseline` with `Operation=Scan` on a daily schedule for compliance, and
  `Operation=Install` (with `RebootOption=RebootIfNeeded`) inside a **maintenance window**
  (`cron(0 2 ? * SUN *)`, cutoff 1 h, rate control) or a **patch policy** from Quick Setup
  across the org.
- Compliance: `list-compliance-summaries`, `describe-instance-patch-states`; non-compliant
  instances surface in Explorer and can trigger EventBridge → ticket.

## 5. State Manager
- An **association** binds a document to targets on a schedule; it reapplies when the instance
  drifts or new instances match the tag. Typical: `AWS-ConfigureAWSPackage` (install
  CloudWatch agent), `AWS-GatherSoftwareInventory`, `AWS-UpdateSSMAgent`, `AWS-RunAnsiblePlaybook`
  / `AWS-ApplyDSCMojoConfiguration` for real config management.
- Compliance type `Association` reports which instances failed the last apply.

## 6. Related building blocks
- **Parameter Store** for config; **Automation** runbooks (`AWS-RestartEC2Instance`,
  `AWS-CreateImage`) for multi-step ops with approvals; **Inventory** + **Fleet Manager**
  for software lists and a browser file explorer; **OpsCenter** for incidents.
- **Quick Setup** → host management for an OU in one go (agent updates, inventory,
  CloudWatch agent, Default Host Management Configuration).

## Gotchas
- Private subnet without the three endpoints = agent never registers; the classic cause.
- Session Manager logging needs the instance role to have `s3:PutObject`/`logs:PutLogEvents`
  — missing permissions make sessions start but transcripts silently vanish.
- `max-errors 0` stops at the first failed instance but does not revert ones already done.
- Patch Manager counts a patch as "missing" when it is *released* and *approved*; a 7-day
  approval delay shows as compliant for 7 days — set it to your policy, not the default.
- Windows reboots inside a maintenance window cutoff can be cut mid-install; leave headroom.
- Unconfirmed: exact Default Host Management Configuration behaviour on instances that already have a conflicting profile — test first.

## Verify
- [ ] Every instance appears in `describe-instance-information` with `PingStatus=Online`.
- [ ] Inbound 22/3389 removed; `start-session` works from a laptop with no public IP on the instance.
- [ ] A session transcript appears in the CloudWatch log group within a minute of closing.
- [ ] `send-command` to a tag of 20 instances with `--max-concurrency 10%` proceeds in waves.
- [ ] Patch compliance summary shows 0 critical missing after the maintenance window.
- [ ] Kill the CloudWatch agent on a host; the State Manager association reinstalls it on next apply.
