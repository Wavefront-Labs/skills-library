---
id: computing-software.cloud-infrastructure-engineering.azure.microsoft-sentinel-connectors-analytics-rules-and-playbooks
name: microsoft-sentinel-connectors-analytics-rules-and-playbooks
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, sentinel, microsoft-sentinel, siem, soar, data-connectors, analytics-rules, scheduled-rules, nrt-rules, fusion, anomaly-rules, incidents, entity-mapping, automation-rules, playbooks, logic-apps, watchlists, threat-intelligence, hunting-queries, workbooks, content-hub, mitre-attack, unified-security-operations, defender-xdr, sentinel-cost, data-collection-rules, codeless-connector, sentinel-repositories, sentinel-playbooks]
level: advanced
status: draft
description: "Stand up Microsoft Sentinel: Content Hub solutions, data connectors, analytics rules with entity mapping and MITRE tags, automation rules and Logic App playbooks, watchlists, cost controls, repos."
sources: ["Microsoft Learn - Microsoft Sentinel overview, onboarding and the unified security operations platform", "Microsoft Learn - Data connectors (Entra ID, Azure Activity, Defender XDR, Syslog/CEF via AMA, codeless connector framework)", "Microsoft Learn - Create scheduled and NRT analytics rules, entity mapping, Fusion and anomaly rules", "Microsoft Learn - Automation rules and playbooks (Logic Apps) in Microsoft Sentinel", "Microsoft Learn - Manage Sentinel content as code with repositories; reduce costs for Microsoft Sentinel"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft Sentinel — connectors, detections and automation that an analyst can run

**Goal:** the right logs flowing (and only those), detections mapped to entities and
MITRE so incidents are triageable, automation that enriches and contains without
paging for noise, and all of it deployed from Git.

## 1. Foundation
```bash
az extension add -n sentinel
az monitor log-analytics workspace create -g rg-sec -n law-sec-prod -l uksouth --retention-time 90
az sentinel onboarding-state create -g rg-sec --workspace-name law-sec-prod -n default      # enables Sentinel on the workspace
# content is managed through Content Hub / portal / Bicep (Microsoft.SecurityInsights/* : alertRules, automationRules, dataConnectors, watchlists); the az extension is thin
```
- One Sentinel workspace per tenant region/compliance boundary; **Content Hub** installs *solutions* (connector + rules + workbooks + hunting queries per product: Microsoft Entra ID, Azure Activity, Defender XDR, Windows Security Events, Syslog, CEF, Palo Alto, Fortinet, Okta…). Install the solution, then enable its connector and rule templates — don't hand-craft what a solution ships.
- Pricing: per-GB analytics ingestion (Sentinel + Log Analytics) or **commitment tiers** (100 GB/day+); free ingestion for Azure Activity, Defender XDR alerts and Office 365 activity (Entra sign-in/audit logs are billed); **Basic/Auxiliary** tables for high-volume logs you only need for hunting/compliance (firewall allow logs, DNS) with **summary rules** feeding analytics.
- **Unified SecOps** (Defender portal): Sentinel surfaces inside security.microsoft.com with Defender XDR — incidents correlate across both; onboard the workspace to the Defender portal once the connector is in place.
- RBAC: *Microsoft Sentinel Reader/Responder/Contributor*, *Sentinel Playbook Operator*, *Automation Contributor* on the playbook RG for Sentinel's identity; workspace **resource-context** access for app teams; table-level RBAC for sensitive tables.

## 2. Connectors (what to turn on first)
| Source | Connector | Notes |
|---|---|---|
| Entra ID | Microsoft Entra ID (diagnostic settings) | `SignInLogs`, `AuditLogs`, `NonInteractiveUserSignInLogs`, `ServicePrincipalSignInLogs`, `ManagedIdentitySignInLogs`, `RiskyUsers`, `UserRiskEvents` — P1/P2 licence |
| Azure control plane | Azure Activity (Policy-driven diagnostic settings at MG scope) | free ingestion; covers every subscription |
| Defender XDR | Microsoft Defender XDR (incidents + raw hunting tables `DeviceEvents`, `EmailEvents`…) | bidirectional incident sync; raw tables are billed |
| Defender for Cloud | subscription-based connector | security alerts/recommendations |
| Office 365 | Office 365 | Exchange/SharePoint/Teams activity (free) |
| Windows servers | Windows Security Events via AMA (DCR with *Common*/*Minimal*/custom xpath) | Arc for on-prem |
| Linux/network/firewalls | **Syslog**/**CEF via AMA** (log forwarder VM/Arc with rsyslog → AMA DCR; CEF to `CommonSecurityLog`) | size the forwarder; use `Syslog` facility filters |
| Azure Firewall / WAF / Key Vault / SQL | diagnostic settings → resource-specific tables; solutions ship the rules | |
| SaaS/APIs | codeless connector framework (CCF) solutions, Logs Ingestion API, Azure Functions-based connectors | |
Validate each with its *Data received* graph and a KQL `count` after 1 h; alert on **connector silence** (`Heartbeat`-style query per table: `union withsource=T * | summarize max(TimeGenerated) by T | where max_ < ago(2h)`).

## 3. Analytics rules
- **Scheduled** (KQL every N min over a lookback, threshold, grouping, suppression), **NRT** (near-real-time, 1-min, simpler KQL), **Microsoft security** (promote Defender/MDI/MCAS alerts to incidents), **Fusion** (ML multi-stage correlation — on by default), **Anomaly** (UEBA-based, tune thresholds), **Threat Intelligence** (TI match on indicators).
- Enable rule **templates** from installed solutions (filter by *Required data connectors* satisfied); review **entity mapping** (Account, Host, IP, URL, FileHash, AzureResource — the join keys for incidents, UEBA and playbooks), **MITRE tactics/techniques**, severity, **alert grouping** (per entity for 5 h) and **incident creation** settings; custom details for fields analysts need in the incident without opening the query.
- Writing your own: `let` thresholds as parameters, `| extend AccountCustomEntity = UserPrincipalName`-style mapping via the UI, test with *Results simulation*, start as **informational** severity with no incident creation for a week, then promote. Keep queries under 30 s; use `materialize()`, time-bounded joins, watchlists for allow-lists (`_GetWatchlist('vip-users')`).
```kusto
// example: privileged role assignment outside PIM, mapped to Account/AzureResource
AuditLogs | where OperationName == "Add member to role" and Result == "success"
| extend Role = tostring(TargetResources[0].modifiedProperties[1].newValue), Target = tostring(TargetResources[0].userPrincipalName), Actor = tostring(InitiatedBy.user.userPrincipalName)
| where Role has_any ("Global Administrator","Privileged Role Administrator") and InitiatedBy.app.displayName != "MS-PIM"
| project TimeGenerated, Actor, Target, Role, CorrelationId
```
- Hygiene: every rule has an owner, a runbook link in the description, and a tuning history; disable noisy templates rather than letting analysts ignore them; **tuning** via automation rules (suppress with conditions) or watchlist exclusions, not by deleting entity mapping.

## 4. Automation: rules and playbooks
- **Automation rules** (ordered, conditions on incident/alert properties, analytics rule names, entities, tags) run on incident creation/update: assign owner/severity, add tags/tasks, close known-benign (e.g. "VPN from office IP"), and **run playbooks**. They're also where suppression/tuning lives (with an expiry date).
- **Playbooks** = Logic Apps (Consumption or Standard) with the *Microsoft Sentinel* trigger (incident/alert/entity) and connector actions: enrich (VirusTotal, GeoIP, Entra user details, Defender device info → incident comment), notify (Teams adaptive card with *Approve block* buttons), contain (disable user via Graph, require re-register MFA, isolate device via Defender for Endpoint, block IP on Azure Firewall/NSG, revoke sessions), ticket (ServiceNow/Jira with incident URL, bidirectional sync).
- Sentinel's identity needs *Microsoft Sentinel Automation Contributor* on the playbook RG; the playbook's managed identity needs *Sentinel Responder* (to comment/close) + the permissions for each action (Graph `User.ReadWrite.All` for disable — scope with PIM-style approval playbooks for destructive actions).
- Incident **tasks** (checklist per rule type) via automation rules; **entity pages** and UEBA (enable *Entity behavior* with Entra/Activity/Security events) for investigation; **hunting** queries with bookmarks → incidents; **workbooks** for coverage (MITRE heat map), connector health, cost.
- SOAR safety: destructive playbooks require an analyst click (Teams approval) unless the rule is high-confidence; log every action to the incident; playbooks in the *playbook* RG with their own alerts on failed runs.

## 5. Content as code and cost
- **Repositories** (Sentinel → Content management → Repositories): connect Azure DevOps/GitHub; export rules/playbooks/workbooks/automation rules/hunting queries as ARM (`az rest` export or the *Export* button), commit, and Sentinel deploys on push via a generated pipeline; branch per environment; PR review for detections. Alternatively Bicep modules for `Microsoft.SecurityInsights/alertRules@2024-...` with `query: loadTextContent('rules/priv-role.kql')`.
- Cost controls: `Usage` by table (log-analytics skill); DCR transformations to drop noise (decide which `SecurityEvent` IDs you really need — 4688 process creation is the big one — and filter Syslog severities); Basic/Auxiliary plans for raw firewall/DNS/proxy; retention 90 days analytics + archive to 1–2 years; commitment tier at scale; Defender XDR raw tables only for the hunting you'll actually do; **Sentinel cost workbook** for trend and per-connector attribution; alert on daily ingestion anomalies.
- Health: *Settings → Health monitoring* on (`SentinelHealth` table: connector/rule/automation failures) → analytics rule on failures; the *Analytics health* and *Automation health* workbooks.

## Gotchas
- A scheduled rule with a 5-min frequency and 5-min lookback misses ingestion lag (Entra ~5–10 min); use lookback ≥ 2× frequency or `ingestion_time()`-aware queries; **event grouping = all events** on a chatty query floods incidents.
- Entity mapping on the wrong column (display name instead of UPN/SID) breaks UEBA/correlation silently; incidents then show unrelated entities.
- Playbook trigger "when an incident is created" fires per incident; alert-trigger playbooks per alert — grouping settings change how many times your containment runs.
- Connectors that rely on diagnostic settings (Entra, Activity, Azure services) die quietly when someone edits the setting — the connector-silence alert is mandatory.
- Defender XDR connector + Microsoft security rules for the same products = duplicate incidents; after XDR integration, disable the overlapping *Microsoft security* rules (the portal warns).
- Automation rules order: a "close benign" rule above the "run enrichment" rule means enrichment never runs on closed incidents — intended; the opposite order wastes playbook runs.
- Repositories deploy **everything in the branch**; a half-written rule in Git becomes a half-working rule in prod — use a `dev` workspace/branch.

## Verify
- [ ] Connector health: every expected table has data < 1 h old; `SentinelHealth` shows no failing connectors; connector-silence rule fires when a diagnostic setting is removed in a test.
- [ ] Simulated attack (e.g. add a test user to Global Admin outside PIM, or Atomic Red Team on a test VM): the rule creates an incident within the frequency window, entities resolved (Account/Host), MITRE technique set, tasks populated, enrichment playbook comment present.
- [ ] Containment playbook with Teams approval disables the test account only after approval; action logged in the incident; failed-run alert tested.
- [ ] Rules/playbooks/automation rules deploy from the repository on PR merge; `Usage` by table reviewed this month with Basic/Auxiliary applied to the top-volume non-detection tables.
