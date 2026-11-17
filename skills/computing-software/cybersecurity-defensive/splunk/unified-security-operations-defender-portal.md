---
id: computing-software.cybersecurity-defensive.splunk.unified-security-operations-defender-portal
name: unified-security-operations-defender-portal
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [microsoft-sentinel, unified-security-operations, defender-xdr, microsoft-defender-portal, advanced-hunting, incident-management, siem-xdr]
level: practitioner
status: docs-checked
description: "Onboard Microsoft Sentinel to the unified security operations platform in the Defender portal: prerequisites, incident merge behaviour, advanced hunting and changes for SOC."
sources: ["https://learn.microsoft.com/en-us/unified-secops-platform/overview-unified-security", "https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal", "https://learn.microsoft.com/en-us/unified-secops-platform/microsoft-sentinel-onboard"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unified security operations in the Defender portal

Microsoft moves Sentinel into the Defender portal (security.microsoft.com) so SIEM and XDR share
one incident queue, hunting and automation. 

## Prerequisites
- A Sentinel workspace; onboarding needs at least Security Administrator in Microsoft Entra ID plus Owner (or User Access Administrator and Microsoft Sentinel Contributor) on the workspace scope; see the onboarding page for the exact table.
- The Defender portal supports a primary workspace and multiple secondary workspaces in one Entra tenant.

## What changes
- **Incidents**: Sentinel alerts correlate with XDR alerts into Defender incidents.
- **Advanced hunting**: query Sentinel tables and XDR tables (DeviceProcessEvents etc.) in one
  place; custom detections can use both.
- **Analytics rules, watchlists, workbooks**: available under Microsoft Sentinel in the portal nav.

## Migration steps
1. Inventory automation rules and playbooks and check which depend on how incidents are named or created.
2. Onboard the workspace by following the onboarding page and choose the primary workspace.
3. Run both portals in parallel; confirm incident counts and SLAs match.
4. Retrain analysts on Defender queue filters, and move SOC dashboards.

## Gotchas
- API consumers using `SecurityIncident` should read `ProviderIncidentId`, the ID assigned by the incident provider.

## Verify
A test alert from a Sentinel analytics rule and a Defender for Endpoint test alert on the same
device correlate into one incident in the Defender portal and sync status to `SecurityIncident`.

## Checked

Date: 2026-10-28

- Confirmed in the onboarding page: one Entra tenant, a primary workspace plus multiple secondary workspaces, onboarding needs at least Security Administrator in Entra plus Owner (or User Access Administrator and Microsoft Sentinel Contributor); SecurityIncident has ProviderIncidentId ("incident ID assigned by the incident provider").
- Removed (not found): Azure portal retirement statement, incident-creation-rule and renaming behaviour, the 30 day hunting retention figure, data lake tier, portal click path, duplicate-incident gotcha.
Method: documentation only; no commands were run.

