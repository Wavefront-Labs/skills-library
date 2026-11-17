---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-webjobs-continuous-and-triggered
name: app-service-webjobs-continuous-and-triggered
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service, webjobs, background-jobs, cron-schedule, always-on]
level: practitioner
status: docs-checked
description: "Run background work in App Service WebJobs: continuous vs triggered jobs, settings.job CRON and singleton, Always On, deployment layout, CLI control and graceful shutdown."
sources: ["https://learn.microsoft.com/en-us/azure/app-service/webjobs-create", "https://learn.microsoft.com/en-us/azure/app-service/webjobs-dotnet-deploy-vs", "https://learn.microsoft.com/en-us/cli/azure/webapp/webjob"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service WebJobs

**Goal:** run scripts or console apps alongside a web app on the same plan, reliably.

## Types
| Type | Runs | Notes |
|---|---|---|
| Continuous | Starts immediately when created; the program must keep running | Runs on **all instances** of the web app unless restricted to a single instance |
| Triggered (manual) | Only when triggered manually | Runs on a single instance Azure selects |
| Triggered (scheduled) | CRON in `settings.job` or the portal | Enable Always On for reliable scheduling |

## Layout and settings
Deploy with the app under `App_Data/jobs/continuous/<name>/` or `App_Data/jobs/triggered/<name>/` (a zip containing the script or program). On Windows code apps the supported types are `.cmd`, `.bat`, `.exe`, `.ps1`, `.sh`, `.js` and `.jar` (Linux and container apps have their own lists in the docs). `settings.job` at the root of the WebJob:
```json
{ "schedule": "0 */15 * * * *", "is_singleton": true, "stopping_wait_time": 60 }
```
CRON has **six** fields (NCRONTAB, seconds first). `is_singleton` applies to continuous jobs; `stopping_wait_time` controls shutdown behaviour.

## Operate
```bash
az webapp webjob continuous list -g rg -n app-orders -o table
az webapp webjob continuous stop  -g rg -n app-orders --webjob-name sync-worker
az webapp webjob continuous start -g rg -n app-orders --webjob-name sync-worker
az webapp webjob triggered run -g rg -n app-orders --webjob-name nightly-report
az webapp webjob triggered log -g rg -n app-orders --webjob-name nightly-report
```
Logs and history: portal WebJobs > Logs. `WEBJOBS_STOPPED=1` stops all WebJobs on the site; `WEBJOBS_DISABLE_SCHEDULE=1` disables triggered jobs
(mark them as deployment slot settings on staging so jobs don't double-run there and the settings don't swap).

## Reliability
- Enable **Always On** (available in Basic, Standard and Premium) for reliable scheduling and continuous jobs.
- Graceful shutdown is controlled with `stopping_wait_time`; see the Kudu WebJobs documentation for the shutdown notification mechanism.
- WebJobs share CPU/memory with the web app - heavy jobs hurt request latency; use a separate plan or move to
  Azure Functions / Container Apps jobs for event-driven or heavy batch work.

## Gotchas
- Continuous jobs on a scaled-out app run on every instance - use `is_singleton` or design for concurrency (multi-instance scale is not available on Free or Shared tiers).
- Deployment slots: jobs run in every slot unless stopped there.

## Verify
- [ ] Scheduled job history shows runs at expected times; continuous job survives an app restart; staging slot has jobs stopped.

## Checked
Checked 2026-10-24 against azure-docs app-service pages (webjobs-create and its webjob-types and file-types includes, webjobs-dotnet-deploy-vs) and the azure-docs-cli webapp webjob reference (continuous list, start, stop; triggered run, log exist). Confirmed: continuous jobs run on all instances unless singleton, triggered jobs on one instance Azure selects; settings.job keys schedule, is_singleton, stopping_wait_time; App_Data/jobs/continuous and triggered folders; NCRONTAB six fields; Always On in Basic, Standard and Premium; WEBJOBS_STOPPED and WEBJOBS_DISABLE_SCHEDULE with deployment slot settings; Windows code file types. Removed unconfirmed: the Kudu azurejobs URL, WEBJOBS_SHUTDOWN_FILE behaviour, time zone settings, the Linux differences note.

Method: documentation only; no commands were run.
