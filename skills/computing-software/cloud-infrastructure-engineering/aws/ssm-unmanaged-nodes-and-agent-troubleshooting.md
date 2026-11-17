---
id: computing-software.cloud-infrastructure-engineering.aws.ssm-unmanaged-nodes-and-agent-troubleshooting
name: ssm-unmanaged-nodes-and-agent-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, systems-manager, ssm-agent-troubleshooting, unmanaged-instance, ssm-endpoints, instance-profile, default-host-management]
level: practitioner
status: docs-checked
description: "Fix EC2 instances missing from Systems Manager: agent status, IAM (instance profile or DHMC), network path to ssm/ssmmessages/ec2messages, and the diagnose tool."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/fleet-manager-troubleshooting-managed-nodes.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent-logs.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-create-vpc.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/remediating-unmanaged-instances.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/diagnosing-ec2-category-types.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent-status-and-restart.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/fleet-manager-default-host-management-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSM unmanaged nodes and agent troubleshooting

A node is available in Systems Manager lists only if (1) SSM Agent is installed and running on a supported OS,
(2) for EC2, an IAM instance profile is attached (or DHMC supplies a role), and (3) the agent can reach a Systems
Manager endpoint; after registration the service sends a signal every five minutes to check health. A node in
Connection Lost status for at least 30 days might drop out of the Fleet Manager console until the cause is fixed.
Check registration (no results until registration succeeds; an empty `InstanceAssociationStatusInfos` means not yet
registered, so troubleshoot if still empty after about 5 minutes):
```bash
aws ssm describe-instance-associations-status --instance-id i-0abc
```

## 1. Use the built-in diagnosis
The Systems Manager console can run a manual or scheduled diagnosis of EC2 instances that are not managed, grouped by
VPC, and either run an Automation execution to remediate or point to manual instructions. The Impacted nodes count
covers instances in Running, Stopped or Stopping state at scan time and is not dynamic (it reflects the last scan).
Diagnosable categories: security group and HTTPS (outbound 443 on the instance; inbound 443 on the `ssm`,
`ssmmessages`, `ec2messages` endpoint security groups), DNS support and hostnames on the VPC, VPC endpoints, network
ACLs (outbound 443; inbound ephemeral ports 1024-65535, since NACLs are stateless), IAM roles and permissions, SSM
Agent version, instance status checks, OS configuration (read from console output), DHMC, and hybrid activations. Some
are diagnose-only with no runbook.

## 2. Checklist
1. **Agent installed and running.** Some AWS managed AMIs include it; a custom AMI can be configured to. Status:
   - Amazon Linux 2/2023, Debian, Oracle Linux, RHEL, SLES: `sudo systemctl status amazon-ssm-agent`; start with
     `sudo systemctl enable amazon-ssm-agent` then `sudo systemctl start amazon-ssm-agent`.
   - Ubuntu Server: `sudo systemctl status snap.amazon-ssm-agent.amazon-ssm-agent.service`; start with
     `sudo snap start amazon-ssm-agent`.
   - Windows Server (PowerShell): `Get-Service AmazonSSMAgent`; start with `Start-Service AmazonSSMAgent`.
   - Logs: `/var/log/amazon/ssm/` on Linux and macOS, `%PROGRAMDATA%\Amazon\SSM\Logs\` on Windows.
2. **Identity.**
   - Instance profile whose role has `AmazonSSMManagedInstanceCore` (or a custom policy with the same permissions).
   - Or **Default Host Management Configuration** (DHMC), turned on per account and Region, which creates and applies a
     default role so instances need no profile. Requires IMDSv2 and SSM Agent 3.2.582.0 or later; it can take up to
     30 minutes for instances to use the role. Setting id:
     `arn:aws:ssm:<REGION>:<ACCOUNT_ID>:servicesetting/ssm/managed-instance/default-ec2-instance-management-role`, value
     `service-role/AWSSystemsManagerDefaultEC2InstanceManagementRole` (managed policy
     `AmazonSSMManagedEC2InstanceDefaultPolicy`, trust principal `ssm.amazonaws.com`).
   - If the instance has its own profile that allows `ssm:UpdateInstanceInformation`, the agent uses the profile
     instead of DHMC, so remove that permission to rely on DHMC.
3. **Network.** Interface endpoints `com.amazonaws.<REGION>.ssm`, `ec2messages` and `ssmmessages`, or outbound HTTPS
   (443) to `ssm.<REGION>.amazonaws.com`, `ssmmessages...` and `ec2messages...`. IPv6-only environments need the
   `*.api.aws` names. The endpoint security group must allow inbound 443 from the instance subnet; with a custom DNS
   server add a conditional forwarder for `amazonaws.com` to the Amazon DNS server. Also `com.amazonaws.<REGION>.s3`
   (agent updates), and optionally `kms` (Session Manager or Parameter Store encryption) and `logs` (CloudWatch Logs).
   No inbound firewall rules are needed because the agent initiates connections.
4. **Proxy** configured correctly for the agent, or the node cannot reach endpoints.
5. **TLS certificate** from Amazon Trust Services must be present (Amazon Root CA 1, Starfield Services Root CA - G2 or
   Starfield Class 2 CA). Test with `curl -L https://ssm.<REGION>.amazonaws.com`: it should return an
   `UnknownOperationException`, not an SSL/TLS error.
6. **Same Region** as the instance in the console or CLI, and the operation supports the node's OS.
7. **Hybrid nodes:** check the activation has not expired or hit its registration limit, and deregister an original VM
   before registering its clone.

## 3. Debug logging
Copy `seelog.xml.template` to `seelog.xml` (`/etc/amazon/ssm/` on most Linux; copy from
`/snap/amazon-ssm-agent/current/` on Ubuntu 18.04/20.04 snap installs; `%PROGRAMFILES%\Amazon\SSM\` on Windows),
change `minlevel` from `info` to `debug`, and restart the agent.

## Verify
- [ ] `describe-instance-associations-status` returns associations for the instance.
- [ ] The node appears in Fleet Manager; DHMC or the instance profile is standardised across the fleet.

## Checked
2026-11-08. Confirmed against the Systems Manager User Guide pages cited above. Removed: the
`AWSSupport-TroubleshootManagedInstance` runbook name, agent log error strings, clock-skew and IMDS hop-limit
claims, the `describe-instance-information` query and the `start-session` check, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
