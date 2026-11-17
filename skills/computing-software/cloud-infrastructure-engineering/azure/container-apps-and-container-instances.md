---
id: computing-software.cloud-infrastructure-engineering.azure.container-apps-and-container-instances
name: container-apps-and-container-instances
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-apps, aca, keda, dapr, container-instances, aci, container-groups, scale-to-zero, revisions, traffic-splitting, ingress, consumption-workload-profile, dedicated-workload-profile, container-apps-environment, container-apps-jobs, managed-identity, acr-pull, internal-ingress, custom-domains, serverless-containers, sidecars]
level: practitioner
status: gated
description: "Serverless containers: Container Apps (environments, revisions, KEDA scale-to-zero, Dapr, jobs, ingress/traffic split, workload profiles) and Container Instances for one-off groups."
sources: ["https://learn.microsoft.com/en-us/azure/container-apps/overview", "https://learn.microsoft.com/en-us/azure/container-apps/environment", "https://learn.microsoft.com/en-us/azure/container-apps/workload-profiles-overview", "https://learn.microsoft.com/en-us/azure/container-apps/networking", "https://learn.microsoft.com/en-us/azure/container-apps/custom-virtual-networks", "https://learn.microsoft.com/en-us/azure/container-apps/containers", "https://learn.microsoft.com/en-us/azure/container-apps/health-probes", "https://learn.microsoft.com/en-us/azure/container-apps/revisions", "https://learn.microsoft.com/en-us/azure/container-apps/scale-app", "https://learn.microsoft.com/en-us/azure/container-apps/jobs", "https://learn.microsoft.com/en-us/azure/container-apps/ingress-overview", "https://learn.microsoft.com/en-us/azure/container-apps/managed-identity-image-pull", "https://learn.microsoft.com/en-us/azure/container-apps/dapr-overview", "https://learn.microsoft.com/en-us/cli/azure/containerapp", "https://learn.microsoft.com/en-us/cli/azure/container"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container Apps and Container Instances — serverless containers, chosen correctly

**Goal:** HTTP services and workers that scale to zero, blue/green by revision, pull from
ACR with identity, and batch containers that run and vanish.

## 1. Which service
| Need | Use |
|---|---|
| Microservices/APIs/workers, autoscale incl. zero, revisions, Dapr | **Container Apps** |
| Scheduled/event-driven short-lived containers | **Container Apps Jobs** |
| One container group now, no orchestration, sidecar to a VM/pipeline, burst from AKS (virtual nodes) | **Container Instances** |
| Full Kubernetes API, operators, CRDs, GPUs at scale | AKS (see aks skills) |

## 2. Container Apps environment
```bash
az containerapp env create -n cae-prod -g rg -l uksouth \
  --infrastructure-subnet-resource-id <subnet, /27 minimum, delegated to Microsoft.App/environments> --internal-only false \
  --logs-destination log-analytics --logs-workspace-id <id> --logs-workspace-key <key> \
  --enable-workload-profiles
az containerapp env workload-profile add -n cae-prod -g rg --workload-profile-name d4 --workload-profile-type D4 --min-nodes 1 --max-nodes 5
```
- **Consumption** profile: serverless, billed on resources used, scales out and optionally to zero.
  **Dedicated** profiles run on reserved compute in your own pool (you choose the VM size and node range) for predictable load.
  Container resource combinations go up to 4.0 vCPU / 8.0 GiB; apps on the Consumption plan in a *Consumption only* environment are limited to 2 cores and 4 GiB.
- VNet-integrated environment: subnet minimum `/27`, delegated to `Microsoft.App/environments` and dedicated to the environment;
  `--internal-only true` = internal environment with no public endpoints (front with App Gateway, or Front Door over private link).
  Workload profiles environments support user-defined routes, egress through NAT Gateway and private endpoints; Consumption-only (legacy) environments do not.
- One environment per trust boundary/VNet; apps in an environment talk by name over the internal DNS.

## 3. Apps, revisions, traffic
```bash
az containerapp create -n api -g rg --environment cae-prod \
  --image myacr.azurecr.io/api:1.4.0 --registry-server myacr.azurecr.io --registry-identity system \
  --ingress external --target-port 8080 --transport auto \
  --min-replicas 0 --max-replicas 20 --cpu 0.5 --memory 1Gi \
  --revision-suffix v1-4-0 --revisions-mode multiple \
  --env-vars DB_CONN=secretref:db-conn --secrets db-conn=keyvaultref:https://kv.vault.azure.net/secrets/db,identityref:<uami-resource-id>
az containerapp ingress traffic set -n api -g rg --revision-weight api--v1-4-0=90 api--v1-3-2=10
az containerapp ingress traffic set -n api -g rg --label-weight blue=0 green=100   # labels for stable URLs
```
- `--registry-identity system|<resource-id>` + *AcrPull* on the registry (the CLI tries to create the role assignment) — no admin credentials.
- Secrets: `keyvaultref:` keeps the value in Key Vault (the identity needs read access to the secret, for example *Key Vault Secrets User*).
- **Single** revision mode = new revision replaces the old once its readiness probe succeeds; **multiple** = several revisions concurrently, with traffic weights and labels (labels are in preview). Inactive revisions are not charged (the total is capped at 100); deactivate with `az containerapp revision deactivate`.
- Ingress: `external` or `internal`, HTTP and TCP ingress types, custom domains, IP restrictions, client certificate mode, session affinity; `--allow-insecure false`.
- Health: `probes` in the YAML/ARM (startup/liveness/readiness) — set them; with ingress enabled the portal adds default TCP probes on the ingress target port (startup: 3 s timeout, 1 s period, failure threshold 240; readiness: 5 s timeout, 5 s period, failure threshold 48).

## 4. Scaling (KEDA)
```bash
az containerapp update -n worker -g rg --min-replicas 0 --max-replicas 50 \
  --scale-rule-name sb --scale-rule-type azure-servicebus \
  --scale-rule-metadata queueName=orders namespace=sb-prod messageCount=20 \
  --scale-rule-identity system
```
Defaults: minimum replicas 0, maximum 10 per revision (configurable up to 1,000). HTTP rules scale on concurrent requests (calculated over 15 seconds); custom rules take KEDA scaler definitions; authentication uses Container Apps secrets or a managed identity (`--scale-rule-identity system` or a resource ID). Set minimum replicas to 1 or higher to keep an instance always running for latency-sensitive APIs.

## 5. Jobs and Dapr
- Jobs: `az containerapp job create --trigger-type Schedule --cron-expression "0 2 * * *"`
  or `--trigger-type Event` (KEDA scaler creates executions per message) or `Manual`
  (`az containerapp job start`). Parallelism, `--replica-retry-limit` and `--replica-timeout` are job settings.
- Dapr: `--enable-dapr --dapr-app-id api --dapr-app-port 8080`; components (state store,
  pub/sub, secrets, bindings) at environment scope (`az containerapp env dapr-component set`),
  scoped to apps. Service invocation through the sidecar (HTTP port 3500) uses automatic mTLS.

## 6. Container Instances
```bash
az container create -g rg -n job-01 --image myacr.azurecr.io/etl:2.0 --acr-identity <uami-id> --assign-identity <uami-id> \
  --cpu 2 --memory 4 --restart-policy Never --os-type Linux \
  --subnet <subnet-id> --azure-file-volume-account-name st --azure-file-volume-share-name data --azure-file-volume-mount-path /data \
  --environment-variables RUN_ID=42 --secure-environment-variables TOKEN=<from KV in pipeline>
az container logs -n job-01 -g rg --follow; az container exec -n job-01 -g rg --exec-command /bin/sh
```
Container groups share a lifecycle, network and volumes; ACI has no autoscale and no revisions, and deploying into a VNet needs a delegated subnet (gated: unconfirmed, source is paywalled or blocked). The Container Instances documentation is not in the public azure-docs repository and was not fetched; the az container flags above were checked against the CLI reference.

## Gotchas
- The ingress target port must match the port the app actually listens on (see the target port troubleshooting article).
- CPU and memory must be a valid combination from the documented table (for example 2.0 vCPU with 4.0 Gi; maximum 4.0 vCPU with 8.0 Gi).
- In multiple revision mode wait for the new revision's readiness probes to succeed before shifting traffic.

## Verify
- [ ] `az containerapp show --query "properties.{fqdn:configuration.ingress.fqdn,rev:latestRevisionName,state:provisioningState}"` → Succeeded, FQDN serves 200.
- [ ] Scale test: queue 1 000 messages → replicas rise to the computed count and return to 0 within the cooldown (`ContainerAppSystemLogs` shows scaling events).
- [ ] Traffic split visible in logs (10 % hits new revision); rollback by weight takes < 1 min.
- [ ] ACI container exits 0, logs captured in Log Analytics, group deleted or restart policy honoured.

## Checked
Checked 2026-10-24 against azure-docs container-apps pages (environment, workload-profiles-overview, networking, custom-virtual-networks, containers, health-probes, revisions, scale-app, jobs, ingress-overview, managed-identity-image-pull, dapr-overview, log-options) and the azure-docs-cli containerapp and container references (all flags and subcommands in the examples exist; --registry-identity and --scale-rule-identity accept system). Confirmed: /27 minimum subnet delegated to Microsoft.App/environments; UDR, NAT Gateway and private endpoints only in workload profiles environments; Consumption-only limit of 2 cores and 4 GiB; default probes; scale defaults 0 and 10; inactive revisions not charged; job trigger types and cron; Dapr sidecar ports and automatic mTLS. Found wrong and fixed: subnet sizing (/27 minimum, not /23), default health probes (startup, liveness and readiness TCP probes, not a single TCP probe), unconfirmed HTTP scale default of 10 concurrent requests removed. Gated: the Container Instances claims (documentation not in the public repository).

Method: documentation only; no commands were run.
