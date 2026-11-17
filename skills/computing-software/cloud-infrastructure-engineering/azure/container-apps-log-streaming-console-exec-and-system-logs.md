---
id: computing-software.cloud-infrastructure-engineering.azure.container-apps-log-streaming-console-exec-and-system-logs
name: container-apps-log-streaming-console-exec-and-system-logs
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-apps, aca-troubleshooting, aca-console, containerappconsolelogs, containerappsystemlogs, revision-failures]
level: practitioner
status: docs-checked
description: "Troubleshoot Azure Container Apps: live log streams, console exec into replicas, system vs console logs in Log Analytics, and the usual causes of failed revisions."
sources: ["https://learn.microsoft.com/en-us/azure/container-apps/log-streaming", "https://learn.microsoft.com/en-us/azure/container-apps/log-options", "https://learn.microsoft.com/en-us/azure/container-apps/container-console", "https://learn.microsoft.com/en-us/azure/container-apps/troubleshooting", "https://learn.microsoft.com/en-us/azure/container-apps/troubleshoot-image-pull-failures", "https://learn.microsoft.com/en-us/azure/container-apps/troubleshoot-container-start-failures", "https://learn.microsoft.com/en-us/azure/container-apps/troubleshoot-health-probe-failures", "https://learn.microsoft.com/en-us/azure/container-apps/troubleshoot-target-port-settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container Apps troubleshooting

**Goal:** go from "revision failed / app returns 5xx" to a root cause quickly.

## Live tools
```bash
az containerapp revision list -g rg -n ca-api -o table          # health, running state, replicas, traffic
az containerapp replica list -g rg -n ca-api --revision <rev> -o table
az containerapp logs show -g rg -n ca-api --type system --follow  # platform events: pulls, probes, scaling
az containerapp logs show -g rg -n ca-api --type console --follow --tail 100
az containerapp exec -g rg -n ca-api --replica <replica> --container api --command /bin/sh
```
`exec` needs a shell in the image (distroless images have none - use a debug image or rely on logs).

## Log destinations
Container Apps writes two log categories, `ContainerAppConsoleLogs` and `ContainerAppSystemLogs`. The environment logs destination can be Log Analytics (the default) or Azure Monitor (diagnostic settings, configurable at environment and app level), and new records can take several minutes to become queryable; use log streaming for real-time output. See the Azure Monitor table reference for the table and column names of your destination.

## Usual causes of failed revisions
| Symptom | Check |
|---|---|
| Image pull failure | Identity lacks AcrPull, wrong registry server, registry not reachable or DNS not resolving from the environment |
| Probe failures | Probe settings, and the ingress target port against the port the app listens on |
| Container exits with a non-zero code | Application logs just before the crash: missing files or dependencies, runtime exceptions |
| No traffic | Ingress disabled or internal only; traffic weights on an old revision |

## Other checks
- *Diagnose and solve problems* blade on the container app.
- Environment VNet: custom DNS must resolve ACR/private endpoints; UDR to firewall must allow ACR/MCR and Azure Monitor endpoints.

## Verify
- [ ] Root cause visible in system logs; new revision healthy with 100% traffic.

## Checked
Checked 2026-10-24 against azure-docs container-apps pages (log-streaming, log-options, container-console, troubleshooting and the troubleshoot-image-pull-failures, container-start-failures, health-probe-failures, target-port-settings articles) and the azure-docs-cli containerapp reference. Confirmed: az containerapp logs show with --type system or console, --follow and --tail; az containerapp exec; distroless images have no shell; log categories ContainerAppConsoleLogs and ContainerAppSystemLogs and the delay before records are queryable; AcrPull for image pull. Removed unconfirmed: _CL table and column names and the KQL queries, the system log reason strings (ErrImagePull, ContainerCrashing, exit code 137, Activating).

Method: documentation only; no commands were run.
