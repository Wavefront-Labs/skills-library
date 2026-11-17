---
id: computing-software.systems-network-administration.patch-management.patch-agent-client-health
name: patch-agent-client-health
category: computing-software
field: systems-network-administration
product: patch-management
tags: [client-health, agent-health, configmgr-client, wsus-client, patch-verification, patch-management]
level: practitioner
status: docs-checked
description: "Keep patch agents healthy: detect clients not reporting (ConfigMgr, SSM, Intune), common root causes, automated remediation and a client health view."
sources:
  - https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/monitor-clients
  - https://docs.aws.amazon.com/systems-manager/latest/userguide/troubleshooting-ssm-agent.html
  - https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-sync
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch agent client health

Compliance reports only cover machines whose agent reports. Unhealthy agents look like "unknown", get filtered out, and hide the worst-patched machines.

## Signals of an unhealthy client
| Tool | Signal |
|---|---|
| ConfigMgr | Client online status (offline if the management point gets no ping-like message for five minutes); client activity (inactive if no policy request, heartbeat or hardware inventory in seven days); client check result |
| AWS SSM | Managed node not showing as online in Systems Manager; the troubleshooting page covers the SSM Agent, endpoints and logs |
| Intune | Device not checking in; the Sync remote action can force a check-in |
| Other tools | Define a "not seen in N days" threshold per tool and write it in the policy |

## ConfigMgr
- Console: Assets and Compliance for per-device online status, Monitoring > Client Status for site-wide client activity and client check charts.
- Client check runs automatically during the Windows maintenance window and can remediate some problems; remediation can be switched off for specific devices such as a business-critical server.
- Alerts can be configured for when client check or activity results drop below a chosen percentage.

## AWS SSM
- SSM Agent needs outbound HTTPS (port 443) to the Systems Manager endpoints for its Region; in a VPC, endpoints must be configured correctly. Check the troubleshooting page for the exact endpoint names (they differ for Regions launched in 2024 and later).
- Other causes listed there: agent out of date, log problems and VPC DNS or security group rules.

## Common root causes (practice advice)
- Disk full, proxy/TLS inspection breaking agent traffic, expired certificates, clock skew.
- Cloned images that share agent identities.

## Automate
- Scheduled remediation that restarts services and reinstalls the agent if broken.
- Cross-check against an independent inventory (directory, EDR, DHCP) to find machines missing from the patch tool entirely.

## Verify
Client health percentage (reporting within the policy threshold / total in the independent inventory) is reported with its denominator; set the target in policy.

## Checked
Date: 2026-11-09. Confirmed against the ConfigMgr "How to monitor clients" page (read in full), the AWS SSM Agent troubleshooting page (endpoint, port 443 and VPC sections, keyword search) and the Intune device sync page (Sync action). Removed: WSUS, Azure Arc and Linux tool thresholds, the PowerShell and AWS CLI queries, WMI and SusClientId repair steps, the 98 percent target and the IAM profile claim, none of which the cited pages state.
Method: documentation only; no commands were run.
