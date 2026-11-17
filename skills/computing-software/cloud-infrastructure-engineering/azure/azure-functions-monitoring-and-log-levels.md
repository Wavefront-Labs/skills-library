---
id: computing-software.cloud-infrastructure-engineering.azure.azure-functions-monitoring-and-log-levels
name: azure-functions-monitoring-and-log-levels
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-functions, functions-monitoring, functions-logging, host-json, application-insights, sampling]
level: practitioner
status: docs-checked
description: "Monitor Azure Functions with Application Insights: host.json log levels and sampling, isolated worker logging filters, invocation queries, log streaming and cost control."
sources: ["https://learn.microsoft.com/en-us/azure/azure-functions/configure-monitoring", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-host-json", "https://learn.microsoft.com/en-us/azure/azure-functions/dotnet-isolated-process-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Functions monitoring and log levels

**Goal:** enough telemetry to debug failures without a runaway Application Insights bill.

## Wire up
App setting `APPLICATIONINSIGHTS_CONNECTION_STRING` (workspace-based App Insights). Optional Entra-authenticated
ingestion with the `APPLICATIONINSIGHTS_AUTHENTICATION_STRING` setting (see the app settings reference for the value format).

## host.json
```json
{
  "version": "2.0",
  "logging": {
    "logLevel": {
      "default": "Warning",
      "Host.Results": "Information",
      "Function": "Information",
      "Function.ProcessOrder.User": "Debug",
      "Host.Aggregator": "Information"
    },
    "applicationInsights": {
      "samplingSettings": { "isEnabled": true, "maxTelemetryItemsPerSecond": 20, "excludedTypes": "Request;Exception" }
    }
  }
}
```
- `Host.Results` = invocation requests (success/failure); `Function.<Name>` = framework logs; `Function.<Name>.User` = your ILogger.
- Exclude Request and Exception from sampling so failures are never sampled away.

## Export options
The built-in Application Insights integration and the OpenTelemetry exporter are both supported; the docs recommend OpenTelemetry with the Azure Monitor exporter for new and existing apps. For .NET isolated apps the guide wires it up with `builder.Services.AddOpenTelemetry().UseFunctionsWorkerDefaults().UseAzureMonitorExporter()` after `FunctionsApplication.CreateBuilder(args)`; `host.json` has a `telemetryMode` setting (`OpenTelemetry`, preview) for the same purpose.

## Queries
```kusto
requests
| where cloud_RoleName == "func-orders" and timestamp > ago(1h)
| summarize count(), failures = countif(success == false), p95 = percentile(duration, 95) by operation_Name
exceptions | where cloud_RoleName == "func-orders" | summarize count() by problemId, outerMessage | top 10 by count_
```
Live: the portal Log stream and Live Metrics for real-time views.

## Cost control
Daily cap on the App Insights/workspace, sampling, `default: Warning`, avoid logging payloads; for chatty triggers
(Event Hubs) raise `Host.Results` to Warning if per-invocation requests are too many.

## Verify
- [ ] Failure invocations visible with exceptions; ingestion volume within budget (check `Usage` table).

## Checked
Checked 2026-10-24 against azure-docs azure-functions pages (configure-monitoring, functions-monitoring, functions-host-json, dotnet-isolated-process-guide). Confirmed: host.json logLevel example (default Warning, Host.Aggregator, Host.Results, Function), Host.Results = requests at Information, Function.<name>.User for user logs, samplingSettings with maxTelemetryItemsPerSecond 20 and excludedTypes Request;Exception, APPLICATIONINSIGHTS_AUTHENTICATION_STRING exists, OpenTelemetry exporter recommended. Removed unconfirmed: the claim that the worker's Application Insights logger adds a Warning filter rule and its code workaround, the func logstream command, the exact Entra connection string value.

Method: documentation only; no commands were run.
