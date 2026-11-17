---
id: computing-software.cloud-infrastructure-engineering.azure.defender-security-alerts-and-incidents-triage
name: defender-security-alerts-and-incidents-triage
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, defender-for-cloud, security-alerts, alert-triage, defender-incidents, defender-xdr, suppression-rules, sample-alerts]
level: practitioner
status: docs-checked
description: "Triage Defender for Cloud security alerts and incidents: severity, MITRE context, take action steps, suppression rules, Defender XDR integration and alert testing."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/managing-and-responding-alerts", "https://learn.microsoft.com/azure/defender-for-cloud/alerts-suppression-rules", "https://learn.microsoft.com/azure/defender-for-cloud/concept-integration-365", "https://learn.microsoft.com/azure/defender-for-cloud/alerts-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security alerts and incidents triage

**Goal:** every Defender for Cloud alert gets a decision (true positive, benign, false positive)
within SLA, with containment steps and tuning to cut noise.

## Where alerts land
- Defender for Cloud → Security alerts (per subscription scope).
- **Defender XDR portal** (security.microsoft.com) — Defender for Cloud alerts are correlated into incidents with MDE, MDI, Entra ID Protection; preferred SOC console.
- Sentinel via the Defender XDR connector.

## Triage steps
1. **Severity** (High/Medium/Low/Informational) and alert **status**. Informational alerts are not integrated into the Defender portal.
2. Read **Alert details**: affected resource, MITRE tactics, entities (IP, account, process), *related alerts* in the incident.
3. **Take action** tab: *Mitigate the threat* steps, *Prevent future attacks* (linked recommendations), *Trigger automated response* (Logic App), *Suppress similar alerts*.
4. Investigate: Activity Log/AzureActivity for control-plane alerts (Defender for Resource Manager), storage logs for Storage alerts, MDE device timeline for server alerts.
5. Contain: isolate VM via MDE, revoke SAS/rotate keys, disable identity, block IP in NSG/firewall.
6. Close with classification.

## Suppression rules (known benign)
```text
Defender for Cloud → Security alerts → Suppression rules → Create:
  Alert type: "Access from a suspicious IP to a storage account"
  Conditions: Entity IP = 203.0.113.10 (pen-test vendor), Resource = st-pentest
  Expiration: 2026-11-30   Reason: Authorized pen test PT-2026-11
```
Rules auto-dismiss matching alerts; keep expiry dates, never suppress by alert type alone across all resources.

## Test the pipeline
Defender for Cloud → Security alerts → **Sample alerts** (per plan) generates test alerts to verify email notifications, workflow automation, Sentinel ingestion and XDR incident creation.

## Notifications
Environment settings → **Email notifications**: roles (Owner) + security DL; minimum severity; attack path notifications (CSPM).

## Query alerts at scale
```kusto
securityresources
| where type == "microsoft.security/locations/alerts"
| where properties.Status == "Active"
| project time = todatetime(properties.TimeGeneratedUtc), sev = tostring(properties.Severity), name = tostring(properties.AlertDisplayName), resource = tostring(properties.ResourceIdentifiers[0].AzureResourceId)
| order by time desc
```

## Gotchas
- Triage in one console to avoid duplicate work; use continuous export if you need alerts kept outside the portal.
- Many "suspicious" control-plane alerts come from automation running from new IPs — fix by using managed identities/known egress rather than broad suppression.

## Verify
- [ ] Sample alert reaches XDR/Sentinel and notifies the DL.
- [ ] No High alerts Active > SLA; all suppression rules have expiry.

## Checked

2026-10-28. Confirmed on the Defender for Cloud alerts and Defender portal integration pages: Informational alerts are not integrated into the Defender portal. Removed: the status flow, bidirectional sync claim and the 90-day alert retention figure (not found in the fetched pages; 90 days there is only a governance time frame). Suppression example values are placeholders.

Method: documentation only; no commands were run.
