---
id: computing-software.cloud-infrastructure-engineering.azure.application-insights-opentelemetry-and-availability-tests
name: application-insights-opentelemetry-and-availability-tests
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-insights, app-insights, opentelemetry, otel, azure-monitor-opentelemetry-distro, distributed-tracing, availability-tests, standard-test, application-map, live-metrics, sampling, adaptive-sampling, workspace-based, connection-string, auto-instrumentation, codeless, failures-blade, performance-blade, smart-detection, workbooks, slo-dashboards, profiler, snapshot-debugger, apm, app-insights-kql, requests-table, dependencies-table]
level: practitioner
status: draft
description: "Instrument apps with Application Insights: workspace-based resources, OpenTelemetry distro vs codeless, sampling for cost, availability tests, application map/failures triage, SLO workbooks."
sources: ["Microsoft Learn - Application Insights overview (OpenTelemetry) and workspace-based resources", "Microsoft Learn - Azure Monitor OpenTelemetry Distro for .NET, Java, Node.js, Python", "Microsoft Learn - Sampling in Application Insights", "Microsoft Learn - Application Insights availability tests (standard tests)", "Microsoft Learn - Application map, Failures and Performance views"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application Insights — traces, requests and dependencies with a bill you control

**Goal:** every service emits correlated telemetry through OpenTelemetry, you can
walk a slow request from Front Door to SQL, synthetic tests prove availability from
outside, and sampling keeps ingestion sane.

## 1. Resource
```bash
az monitor app-insights component create -g rg-mon --app ai-orders-prod -l uksouth --kind web --application-type web --workspace <law-id> --retention-time 90
az monitor app-insights component show --app ai-orders-prod -g rg-mon --query connectionString -o tsv    # APPLICATIONINSIGHTS_CONNECTION_STRING
```
- **Workspace-based** only (classic retired); data lives in Log Analytics tables
  `AppRequests`, `AppDependencies`, `AppExceptions`, `AppTraces`, `AppMetrics`, `AppAvailabilityResults`, `AppPageViews` — same KQL, same retention/plan controls.
- One resource per application per environment; services of one system can share a resource (application map stitches by `cloud_RoleName`), or separate resources with cross-resource queries.
- Connection string, not instrumentation key (keys are deprecated); treat it as config, not secret (it only allows ingestion). For hardened setups set the ARM property `DisableLocalAuth: true` and have the SDK use Entra ingestion auth with a managed identity (*Monitoring Metrics Publisher* role).

## 2. Instrumentation
| Stack | Recommended |
|---|---|
| .NET (ASP.NET Core) | `Azure.Monitor.OpenTelemetry.AspNetCore` → `builder.Services.AddOpenTelemetry().UseAzureMonitor();` |
| Java | Java agent `-javaagent:applicationinsights-agent-3.x.jar` (codeless, OTel-based) with `applicationinsights.json` |
| Node.js | `@azure/monitor-opentelemetry` `useAzureMonitor()` first line of the app |
| Python | `azure-monitor-opentelemetry` `configure_azure_monitor()` |
| App Service / Functions / AKS | **codeless auto-instrumentation** (App Service *Application Insights* blade toggle; Functions built-in; AKS via `az aks ... --enable-azure-monitor-app-monitoring`) — zero code for Java/.NET/Node |
- Set `OTEL_SERVICE_NAME` / `cloud_RoleName` and `service.instance.id` so the map and queries are per service, not per host.
- Add custom spans with the OTel API (`ActivitySource`, `tracer.start_as_current_span`), custom metrics via OTel meters, and structured log scopes — they land in `AppDependencies`/`AppMetrics`/`AppTraces`.
- Propagation is W3C `traceparent` by default: Front Door/App Gateway pass it; Service Bus/Event Hubs SDKs carry it in message properties; Functions continue it automatically.
- Live Metrics (1-s stream, free) for deploy watch; Profiler/Snapshot Debugger (.NET) for CPU traces and exception snapshots in production.

## 3. Sampling (decide before go-live)
- Defaults differ by distro (the .NET distro and Java agent ship *rate-limited* sampling of roughly 5 traces/s; Node/Python send 100 % until you set a rate), and they change between versions — unconfirmed for your version, so never rely on the default.
  Set it explicitly: `OTEL_TRACES_SAMPLER_ARG=0.2` (20 %) or `APPLICATIONINSIGHTS_SAMPLING_PERCENTAGE` (Java).
- Sampling is **trace-level**: all spans of a sampled request are kept together; `itemCount` in tables reflects the weight (`sum(ItemCount)` not `count()` for true totals).
- **Ingestion sampling** (resource *Usage and estimated costs > Data sampling*) as a second lever when you can't redeploy.
- Daily cap on the App Insights resource + alert at 90 %; exceptions and availability results are never sampled by the SDKs.

## 4. Availability tests
```bash
az monitor app-insights web-test create -g rg-mon -n at-orders-health --location uksouth --defined-web-test-name "orders health" \
  --kind standard --enabled true --frequency 300 --timeout 30 --retry-enabled true --web-test-kind standard \
  --locations Id="emea-gb-db3-azr" Id="emea-nl-ams-azr" Id="us-va-ash-azr" Id="apac-sg-sin-azr" Id="emea-fr-pra-edge" \
  --http-verb GET --request-url https://api.example.com/healthz --expected-status-code 200 --ssl-check true --ssl-lifetime-check 30 --tags hidden-link:<ai-id>=Resource
```
- **Standard tests** (HTTP method, headers, body, content match, TLS expiry check) from 5+ regions; alert rule auto-created (`failed locations ≥ 3 of 5` — tune to avoid single-POP flaps).
- Private endpoints: tests run from public POPs — expose a lightweight public health endpoint or use **TrackAvailability()** custom tests from a Function inside the VNet.
- Multi-step web tests are retired; use Playwright/Functions for journeys and emit `availabilityResults`.

## 5. Triage views
- **Application map**: nodes = roles, edges = dependency call rates/latency/failure %; click an edge → samples; a red SQL node with 90 % failures tells you where before you read a log.
- **Failures**: top exceptions/failed dependencies by operation; **Performance**: p50/p95/p99 per operation, *drill into samples* → end-to-end transaction (Gantt of spans across services).
- KQL staples:
```kusto
AppRequests | summarize p95=percentile(DurationMs,95), fail=sumif(ItemCount, Success==false), total=sum(ItemCount) by OperationName | extend errRate=fail*100.0/total | order by p95 desc
AppDependencies | where Success == false | summarize sum(ItemCount) by Target, Type, ResultCode, bin(TimeGenerated,5m)
AppExceptions | summarize n=sum(ItemCount) by ProblemId, OuterMessage | top 20 by n
union AppRequests, AppDependencies, AppTraces | where OperationId == "<id>" | order by TimeGenerated asc   // one transaction
```
- **Smart detection**: failure anomalies and degradation detectors auto-enabled; route via alert rules/action groups.
- Workbooks: start from the *Application Performance*, *Failure Analysis*, *Usage* templates; build an SLO workbook (availability = 1 − errRate, latency SLI = p95 < target) with parameters per role.

## Gotchas
- `count()` on sampled tables under-reports; use `sum(ItemCount)` everywhere that matters.
- Role name missing → every instance of every service is "the app"; map becomes one blob.
- Codeless + SDK both enabled = duplicate telemetry and double cost; pick one per app (App Service shows a warning).
- Dependencies to private endpoints appear by IP unless the SDK resolves names; set `Target` via enrichment or accept IPs.
- Availability test alerts count *locations failed*, not consecutive failures; with 5 locations and threshold 1 you'll page on any POP hiccup.
- Java agent needs the JVM option on **every** process (sidecars, cron jobs) — missing on a batch job = missing traces, no error.
- Retention and plan are set on the workspace tables now; the App Insights `retention-time` applies only to classic leftovers and some views.

## Verify
- [ ] A request through the stack shows one `OperationId` across `AppRequests` → `AppDependencies` (HTTP + SQL) → downstream service `AppRequests`; application map has one node per role with the correct names.
- [ ] `AppRequests | summarize sum(ItemCount), count()` ratio equals the configured sampling rate (e.g. 5:1 at 20 %).
- [ ] Availability test shows 5/5 locations green; breaking the health endpoint fires the alert within 2 test intervals and recovers.
- [ ] Daily ingestion for the resource matches budget; cap alert configured.
