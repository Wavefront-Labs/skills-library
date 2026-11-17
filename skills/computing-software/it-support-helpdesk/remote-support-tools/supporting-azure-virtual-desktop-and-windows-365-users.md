---
id: computing-software.it-support-helpdesk.remote-support-tools.supporting-azure-virtual-desktop-and-windows-365-users
name: supporting-azure-virtual-desktop-and-windows-365-users
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, azure-virtual-desktop, windows-365, cloud-pc, windows-app, avd, fslogix]
level: practitioner
status: draft
description: "Support AVD and Windows 365 users: Windows App feed and assignment checks, host pool and drain mode, Cloud PC restart/restore, connection diagnostics and profile errors."
sources:
  - "https://learn.microsoft.com/en-us/azure/virtual-desktop/troubleshoot-client-windows"
  - "https://learn.microsoft.com/en-us/windows-365/enterprise/troubleshoot-windows-365-boot"
  - "https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics"
  - "https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# supporting-azure-virtual-desktop-and-windows-365-users

## Client side
- Current client is **Windows App** (Windows, macOS, iOS, Android, web at
  `windows.cloud.microsoft`). It shows both AVD desktops/RemoteApps and Cloud PCs.
- No resources listed: user not assigned. AVD needs the user (or group) on an application
  group (Desktop Virtualization User role); Windows 365 needs a licence plus a
  provisioning policy assignment.
- Stale feed: refresh in the client or unsubscribe/resubscribe.

## AVD: "no available resources" / cannot connect
1. Host pool: are session hosts Available, not Unavailable/Needs Assistance, and is
   **drain mode** off on at least one?
2. Max session limit reached on all hosts (breadth vs depth load balancing).
3. Session host agent or SxS stack unhealthy; restart the host or reinstall the agent.
4. Personal host pool: user's assigned VM deallocated and Start VM on Connect not enabled.

## Windows 365
- Restart the Cloud PC from Windows App or `windows365.microsoft.com`.
- **Troubleshoot** action in the portal runs checks and fixes common issues.
- **Restore** to a point-in-time snapshot when an update or change broke it (admin can
  allow user restore). **Reprovision** wipes it; data loss unless OneDrive holds the data.

## Diagnostics
Log Analytics workspace tables `WVDConnections`, `WVDErrors`, `WVDCheckpoints` show each
connection attempt, the stage that failed and the error code. Azure Virtual Desktop
Insights gives the same in workbooks.

## Profile issues
Temporary profile or slow logon on pooled hosts is usually FSLogix (container locked by a
stale session, share permissions, disk full); see fslogix-profile-container-support.

## Gotchas
- RDP Shortpath (UDP) blocked by the network shows as drops and lag, not as failure.
- Multi-factor prompts appear per connection if Conditional Access sign-in frequency
  targets the AVD app; that is policy, not a fault.

## Verify
User sees the desktop in Windows App, connects, and the connection shows Completed in
`WVDConnections` with no matching `WVDErrors` row.
