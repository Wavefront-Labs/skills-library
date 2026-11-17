---
id: computing-software.systems-network-administration.windows-server.system-insights-predictive-capacity
name: system-insights-predictive-capacity
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, performance-monitoring, perfmon, system-insights, predictive-analytics, capacity-forecasting, get-insightscapability, windows-admin-center]
level: practitioner
status: docs-checked
description: "Use System Insights for on-box predictive capacity forecasting: enable capabilities, schedules, results, remediation actions and custom capabilities."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/system-insights/overview
  - https://learn.microsoft.com/en-us/windows-server/manage/system-insights/managing-capabilities
  - https://learn.microsoft.com/en-us/windows-server/manage/system-insights/understanding-capabilities
  - https://learn.microsoft.com/en-us/windows-server/manage/system-insights/adding-and-developing-capabilities
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System Insights predictive capacity

System Insights (Windows Server 2019 and newer; preinstalled) runs local machine-learning models on daily data to
forecast long-term trends in CPU, network, total storage and volume consumption.

## List and enable
```powershell
Get-InsightsCapability
Enable-InsightsCapability -Name 'CPU capacity forecasting'
```
Default capabilities: CPU capacity forecasting, Networking capacity forecasting, Total storage consumption forecasting,
Volume consumption forecasting. Daily inputs: volume size (maximum daily), sum of volume and disk sizes (maximum daily),
% Processor Time and Bytes Total/sec (maximum 2-hour average per day).

## Run and read
```powershell
Invoke-InsightsCapability -Name 'Volume consumption forecasting'
Get-InsightsCapabilityResult -Name 'Volume consumption forecasting'
Get-InsightsCapabilityResult -Name 'Volume consumption forecasting' -History     # last 30 results
$Output = Get-Content (Get-InsightsCapabilityResult -Name 'CPU capacity forecasting').Output -Encoding UTF8 | ConvertFrom-Json
```
Status: Ok (forecast does not exceed capacity), Warning (forecast exceeds capacity in the next 30 days), Critical
(in the next 7 days), Error (unexpected failure), None (not enough data). With 0 to 5 days of data no prediction is
made; 6 to 180 days forecast one third of the input length, 180 to 365 days forecast 60 days. The autoregressive model
needs three weeks of data and a basic linear trend is used until then. With several volumes or adapters the status is
the most severe across them; per-instance detail is in the JSON output.

## Schedules and actions
```powershell
Set-InsightsCapabilitySchedule -Name 'Volume consumption forecasting' -Daily -At 3:00AM
Set-InsightsCapabilityAction -Name 'Volume consumption forecasting' -Type Warning `
  -Action '<vol>:\Scripts\ExtendVolume.ps1' -ActionCredential (Get-Credential)
```
Actions run a script when a capability reports Warning or Critical, using the credentials in `-ActionCredential`;
`Get-InsightsCapabilityAction` lists them and `Remove-InsightsCapabilityAction` deletes one. Periodic predictions are
enabled by default; `Enable-/Disable-InsightsCapabilitySchedule` toggle them.

## Windows Admin Center
The System Insights extension in Windows Admin Center shows capabilities and lets you enable, disable, invoke and
schedule them and set actions. Each finished prediction logs an event in
`Microsoft-Windows-System-Insights/Admin` (Ok 151, Warning 148, Critical 150, Error 149, None 132); Azure Monitor or
System Center Operations Manager can aggregate them across servers.

## Custom capabilities
Capabilities can be added without updating the operating system; see Microsoft's Add and develop capabilities page.

## Verify
- [ ] All capabilities return Ok or an actionable forecast; schedules enabled.

## Checked

2026-10-27. Documentation release: windowsserverdocs System Insights pages (overview 2025-06-02, FAQ 2025-06-09, managing and understanding capabilities, current). Confirmed: version availability, preinstalled, default capabilities and data points, status definitions and 30/7-day thresholds, forecast timelines, three-week model note, cmdlets and schedule syntax, action behaviour, event channel and event IDs, Windows Admin Center support. Removed the System-Insights feature install command (the overview says it is preinstalled), the ForecastingResults property and the '30-ish days' storage statement.

Method: documentation only; no commands were run.
