---
id: computing-software.cloud-infrastructure-engineering.azure.azure-monitor-agent-data-collection-rules-and-vm-insights
name: azure-monitor-agent-data-collection-rules-and-vm-insights
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor-agent, ama, data-collection-rules, dcr, data-collection-endpoint, dce, vm-insights, dependency-agent, performance-counters, syslog, windows-event-logs, custom-text-logs, iis-logs, json-logs, logs-ingestion-api, dcr-association, dcr-transformations, azure-arc, policy-deploy-ama, mma-migration, agent-health, heartbeat]
level: practitioner
status: draft
description: "Collect guest telemetry with Azure Monitor Agent: DCRs for perf/Syslog/Windows events/custom logs, DCEs and private link, Policy-driven associations across VMs and Arc, VM Insights, AMA health."
sources: ["Microsoft Learn - Azure Monitor Agent overview and migration from Log Analytics agent", "Microsoft Learn - Data collection rules in Azure Monitor (structure, DCE, associations)", "Microsoft Learn - Collect text and JSON logs with Azure Monitor Agent", "Microsoft Learn - Enable VM Insights (Dependency agent, Map)", "Microsoft Learn - Troubleshoot the Azure Monitor Agent"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Azure Monitor Agent and DCRs — guest metrics and logs defined once, applied by policy

**Goal:** every VM and Arc server sends exactly the counters, events and app logs you
chose, to the workspace you chose, through rules that live in IaC — with no per-machine
configuration and no retired MMA left behind.

## 1. Model
**Data Collection Rule** (what to collect, transform, where to send) + **DCR association**
(which machines) + optional **Data Collection Endpoint** (needed for custom logs,
Logs Ingestion API, and private link). The agent (`AzureMonitorLinuxAgent` /
`AzureMonitorWindowsAgent` extension) pulls its config from associated DCRs; one agent
can serve many DCRs (and many workspaces — the multi-homing MMA couldn't do cleanly).
```bash
az vm extension set -g rg --vm-name vm --name AzureMonitorLinuxAgent --publisher Microsoft.Azure.Monitor --enable-auto-upgrade true   # managed identity required (system or UAMI via settings)
az monitor data-collection rule create -g rg-mon -n dcr-linux-base -l uksouth --rule-file dcr-linux-base.json
az monitor data-collection rule association create --name vm-base --rule-id <dcr-id> --resource <vm-id>
```
DCR JSON core:
```json
{"location":"uksouth","properties":{
 "dataSources":{
  "performanceCounters":[{"name":"perf","streams":["Microsoft-Perf"],"samplingFrequencyInSeconds":60,
    "counterSpecifiers":["\\Processor(_Total)\\% Processor Time","\\Memory\\Available MBytes","\\LogicalDisk(*)\\% Free Space","\\Network Interface(*)\\Bytes Total/sec"]}],
  "syslog":[{"name":"sys","streams":["Microsoft-Syslog"],"facilityNames":["auth","authpriv","daemon","kern"],"logLevels":["Warning","Error","Critical","Alert","Emergency"]}],
  "windowsEventLogs":[{"name":"win","streams":["Microsoft-Event"],"xPathQueries":["System!*[System[(Level=1 or Level=2 or Level=3)]]","Security!*[System[(EventID=4624 or EventID=4625 or EventID=4672)]]"]}]},
 "destinations":{"logAnalytics":[{"workspaceResourceId":"<law-id>","name":"law"}],"azureMonitorMetrics":{"name":"metrics"}},
 "dataFlows":[{"streams":["Microsoft-Perf"],"destinations":["law","metrics"]},{"streams":["Microsoft-Syslog","Microsoft-Event"],"destinations":["law"],"transformKql":"source | where not(Computer startswith 'build-')"}]}}
```
- `azureMonitorMetrics` destination puts guest counters into **Azure Monitor Metrics** (cheap metric alerts, no ingestion cost) — do this for CPU/mem/disk and keep Logs for events.
- XPath for Windows events (test with `Get-WinEvent -FilterXPath`); Syslog needs the agent's rsyslog/syslog-ng forwarder (`/etc/rsyslog.d/10-azuremonitoragent-omfwd.conf`) that the extension installs.
- Transformations (`transformKql`) drop/mask at the edge of ingestion (see log-analytics skill).

## 2. Custom logs and the ingestion API
- Text/JSON files: DCE + custom table (`az monitor log-analytics workspace table create -n MyApp_CL --columns TimeGenerated=datetime RawData=string ...`) + DCR `logFiles` data source (`filePatterns: ["/var/log/myapp/*.log"]`, `format: text|json`, stream `Custom-MyApp_CL`) with a `transformKql` to parse (`source | extend parsed = parse_json(RawData) | project TimeGenerated=todatetime(parsed.ts), Level=tostring(parsed.level), Message=tostring(parsed.msg)`).
- IIS logs: `iisLogs` data source → `W3CIISLog`.
- **Logs Ingestion API**: `POST https://<dce>.<region>.ingest.monitor.azure.com/dataCollectionRules/<immutableId>/streams/Custom-MyApp_CL?api-version=2023-01-01` with an Entra token (app/managed identity with *Monitoring Metrics Publisher* on the DCR) — replaces the HTTP Data Collector API; the DCR schema + transform validates/shapes rows.
- Events to Event Hubs or Storage directly from AMA (no workspace) for SIEM pipelines.

## 3. VM Insights
`az vm extension set --name DependencyAgentLinux --publisher Microsoft.Azure.Monitoring.DependencyAgent` (or Windows) plus the **VM Insights DCR** (portal creates `MSVMI-<workspace>` with `InsightsMetrics` + `VMConnection`/`VMProcess`/`VMBoundPort`): performance workbook (CPU/mem/disk/net percentiles across the fleet) and **Map** (process-level dependencies — what talks to what on which port). Dependency agent is optional; perf-only VM Insights is `Microsoft-InsightsMetrics` stream alone. `InsightsMetrics` is Analytics-plan data: budget it.

## 4. Deploy at scale
- Policy initiatives: *Deploy Azure Monitor Agent (Linux/Windows) with user-assigned identity* + *Configure ... to be associated with a DCR* (parameter: DCR ID) — with remediation, every VM/VMSS/Arc server in scope gets the agent + association; a `DeployIfNotExists` on new ones.
- A **user-assigned identity** shared across VMs for the agent (`--identity` in the policy params) avoids system-identity sprawl.
- Arc: same extension via `az connectedmachine extension create`; DCR association on the Arc machine resource; outbound to `*.handler.control.monitor.azure.com`, `*.ingest.monitor.azure.com`, `*.ods.opinsights.azure.com` or private link via **Azure Monitor Private Link Scope** + DCE.
- Retire MMA (deprecated Aug 2024): *AMA migration helper* workbook lists machines still sending via MMA; remove `OmsAgentForLinux`/`MicrosoftMonitoringAgent` after confirming DCR data parity (`Heartbeat | summarize by Computer, Category` shows `Azure Monitor Agent` vs `Direct Agent`).

## 5. Troubleshoot
- `Heartbeat | where TimeGenerated > ago(10m) | summarize by Computer, Category, Version` — missing = agent/identity/network.
- Linux: `systemctl status azuremonitoragent`, logs `/var/opt/microsoft/azuremonitoragent/log/mdsd.err`; config received at `/etc/opt/microsoft/azuremonitoragent/config-cache/`; troubleshooter `/var/lib/waagent/Microsoft.Azure.Monitor.AzureMonitorLinuxAgent-*/ama_tst/ama_troubleshooter.sh`.
- Windows: service `AzureMonitorAgent`, `%SystemDrive%/WindowsAzure/Resources/AMADataStore.<vm>/Configuration/` and the `AMA troubleshooter` script in the extension folder.
- Common: no managed identity → agent `Not Ready`; DCR association missing (`az monitor data-collection rule association list --resource <vm-id>`); DCE missing for custom logs; Syslog not arriving because rsyslog isn't installed; Windows XPath typo (event log shows nothing, no error).
- Agent metrics: `AMA`'s own health in *Azure Monitor Agent Health* workbook (heartbeat gaps, version drift).

## Gotchas
- A DCR is regional and must be in the same region as the DCE (not the VM); associations work cross-region.
- Counters collected to both Logs and Metrics are billed for the Logs copy — route high-frequency counters to Metrics only.
- `samplingFrequencyInSeconds` 10 s across 500 VMs = large `Perf` ingestion; 60 s is the sane default, 300 s for capacity trends.
- Security events via AMA require the *Sentinel Windows Security Events* DCR type (`Microsoft-SecurityEvent` stream) — not the generic `Microsoft-Event`.
- Multiple DCRs collecting the same counter = duplicate rows and double billing.
- Auto-upgrade of the extension is strongly recommended; pinned old agents miss DCR features (JSON logs, transformations).

## Verify
- [ ] `Heartbeat` shows `Category == "Azure Monitor Agent"` for every VM/Arc server in scope; zero MMA heartbeats.
- [ ] `Perf | where ObjectName == "Processor" | summarize by Computer` returns all machines; guest CPU appears under *Virtual Machine Guest* metrics namespace for metric alerts.
- [ ] A line written to `/var/log/myapp/test.log` appears in `MyApp_CL` parsed into columns within ~5 min.
- [ ] VM Insights Map shows the app VM's connection to the DB on 1433; Policy compliance for the AMA initiative at 100 %.
