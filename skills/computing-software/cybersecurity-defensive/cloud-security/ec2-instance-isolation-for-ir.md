---
id: computing-software.cybersecurity-defensive.cloud-security.ec2-instance-isolation-for-ir
name: ec2-instance-isolation-for-ir
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-incident-response, ec2-isolation, isolation-security-group, instance-quarantine, ebs-snapshot, memory-capture, automated-forensics-orchestrator, aws]
level: advanced
status: draft
description: "Isolate a compromised EC2 instance for investigation without destroying evidence: tag, isolation security group, detach from ASG/ELB, snapshot, memory capture and role revocation."
sources: ["AWS Security Incident Response User Guide (compute isolation)", "AWS Prescriptive Guidance - Automated Forensic Orchestrator for Amazon EC2", "NIST SP 800-61r3 (containment)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EC2 instance isolation for incident response

**Goal:** stop a compromised instance from talking to anything, keep its state for forensics,
and prevent its credentials from being used, in minutes and in the right order.

## Order of operations
1. **Tag** the instance (`ir-status=quarantine`, case ID) so automation and people know.
2. **Enable termination protection** and set shutdown behaviour to stop:
```
aws ec2 modify-instance-attribute --instance-id i-0abc --disable-api-termination
aws ec2 modify-instance-attribute --instance-id i-0abc --instance-initiated-shutdown-behavior stop
```
3. **Remove from Auto Scaling group** (`aws autoscaling detach-instances --should-decrement-desired-capacity false`) or set it to Standby, and deregister from load balancer target groups, so it is not replaced or terminated.
4. **Network isolation**: replace all security groups with an isolation SG that has no inbound and no outbound rules (or only from the forensic workstation). Existing *tracked* connections survive a security group change; the AWS IR guide's method is to first attach a temporary SG allowing all traffic from/to 0.0.0.0/0 (which makes connections untracked), then swap to the isolation SG so those connections drop. A subnet NACL deny is an alternative when the whole subnet can be isolated.
5. **Revoke the instance role's credentials**: attach a deny policy to the role conditioned on `aws:TokenIssueTime` before now (the IAM console "Revoke active sessions" does this), or detach the instance profile (new credentials stop, issued ones last until expiry).
6. **Capture memory** if needed (SSM Run Command with AVML/LiME to an evidence bucket) before any reboot.
7. **Snapshot EBS volumes**, tag with case ID, copy to the forensic account; analyse on a separate instance.
8. Decide later: terminate or keep, once evidence is preserved and scope is known.

## Automate
Step Functions/Lambda runbooks (AWS Automated Forensic Orchestrator) triggered from GuardDuty
findings or by an analyst, so isolation is consistent and fast.

## Gotchas
- Terminating first destroys memory and instance-store evidence.
- Stopping the instance loses memory; only stop after capture.
- SSM agent communication needs network access to SSM endpoints; isolation SG must allow it via VPC endpoints if you plan to use SSM afterwards.
- Credentials already stolen from IMDS stay valid until revoked; step 5 is essential.

## Verify
- [ ] Runbook tested on a test instance quarterly; timings recorded.
- [ ] After isolation, flow logs show no traffic except the forensic path.
