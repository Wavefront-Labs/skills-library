---
id: computing-software.cloud-infrastructure-engineering.azure.bastion-shareable-links-and-session-recording
name: bastion-shareable-links-and-session-recording
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bastion, bastion-shareable-link, session-recording, bastion-premium, bastion-audit-logs]
level: practitioner
status: docs-checked
description: "Use Bastion shareable links for users without portal access and Premium session recording to a blob container, with limits, storage constraints and permissions."
sources: ["https://learn.microsoft.com/azure/bastion/shareable-link", "https://learn.microsoft.com/azure/bastion/session-recording", "https://learn.microsoft.com/azure/bastion/monitor-bastion"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bastion shareable links and session recording

**Goal:** give a vendor or non-Azure user time-bound access to one VM without an Azure role, and
record privileged sessions for audit.

## Shareable links (Standard SKU or higher)
- The Standard SKU is required. Enable: Bastion -> Configuration -> Tier Standard -> *Shareable Link* -> Apply (about 10 minutes to update).
- Create: Bastion -> Shareable links -> + Add -> select resources (one link per resource) -> Apply. Set an **Expiration** date and time on each link; after it passes the link shows *Link expired* and cannot connect.
- The link contains no credentials: the user opens it, then signs in over RDP or SSH with a username and password or private key, which the admin must supply. Custom ports and protocols are supported.
- The VM must be in the Bastion VNet or a directly peered VNet.
- Limits: 50 shareable-link requests (creates and deletes) at a time and 500 links per Bastion resource.
- Not supported: peered VNets across tenants, Virtual WAN, on-premises or non-Azure VMs.
- Deleting the target resource leaves the link in the list but it fails with a connection error; delete it or keep it for audit.
- Delete a link: Bastion -> Shareable Links -> select -> Delete.
- Permissions are via IAM on the Bastion host. By default users have only Read (use and view links). Creating or deleting needs `Microsoft.Network/bastionHosts/createShareableLinks/action`, `deleteShareableLinks/action` and `deleteShareableLinksByToken/action`; `getShareableLinks/action` is needed to see links.

## Session recording (Premium SKU)
Records graphical RDP and SSH sessions through the bastion host and stores them in a blob container. Considerations from the docs:
- Not available via native client. It cannot be used concurrently with Entra ID support for RDP sessions in the portal.
- Immutable storage policies and blob versioning on the recordings must **not** be present. One container/storage account at a time.
- Once enabled, Bastion records ALL sessions through that host. Viewing recordings needs the Storage Blob Data Reader role.

Setup:
1. Storage account plus a dedicated container. Storage account -> Resource sharing (CORS) -> Blob service rule: allowed origin `https://` plus the full bastion DNS name starting with `bst-` (case-sensitive), allowed methods GET, allowed headers `*`, exposed headers `*`, max age 86400.
2. Enable: Bastion -> Configuration -> Tier Premium -> *Session Recording* -> Apply.
3. Storage access, either a managed identity (recommended, preview at time of writing): turn on the Bastion identity, give it Storage Blob Data Contributor on the storage account, then set it with the Blob Container URI under Session Recording Configuration. Or a SAS URL: container -> Generate SAS with READ, CREATE, WRITE, LIST, start time at least 15 minutes in the past, expiry long into the future, HTTPS only -> Bastion -> Session recordings -> *Add or update SAS URL*.
View: Bastion -> Session recordings -> select VM and recording -> View recording (integrated web player).

## Audit and monitoring
Route Bastion resource logs to Log Analytics with a diagnostic setting; see the Bastion monitoring data reference for the log categories and table schema, and the Azure Monitor activity log for control-plane events.

## Gotchas
- A SAS URL with an expiry in the past stops recordings working; use a long expiry and track it, or prefer the managed identity.
- Recordings can contain sensitive data on screen; restrict container access.
- Because native client sessions are not recorded, block native-client connections where recording is mandatory (check the Bastion configuration for the native client setting).

## Verify
- [ ] Shareable links list reviewed regularly; no links for ended engagements.
- [ ] A test session appears as a playable recording.

## Checked
Date: 2026-10-31. Confirmed against Learn pages "Create a shareable link for Bastion", "Configure Bastion session recording" and "Monitor Azure Bastion": SKU requirements, link expiry, limits (50 requests, 500 links), unsupported scenarios, permissions list, CORS values, SAS permissions and timing, managed identity option, immutability and versioning restrictions, native client and Entra RDP restrictions.
Removed as unconfirmed: the `az rest` createShareableLinks call and api-version, the `az` enable flags, "links don't expire", private-only Bastion link behaviour, the claim that link users bypass Conditional Access, the `MicrosoftAzureBastionAuditLogs` query and its column names, the `bastion-recordings` name and lifecycle-rule/immutability retention advice (the docs forbid immutable policies).
Method: documentation only; no commands were run.
