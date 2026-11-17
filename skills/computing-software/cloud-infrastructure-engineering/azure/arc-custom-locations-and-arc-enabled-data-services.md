---
id: computing-software.cloud-infrastructure-engineering.azure.arc-custom-locations-and-arc-enabled-data-services
name: arc-custom-locations-and-arc-enabled-data-services
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-arc, custom-locations, arc-data-controller, arc-kubernetes, sql-managed-instance-arc, cluster-extensions]
level: advanced
status: docs-checked
description: "Turn an Arc-connected Kubernetes cluster into an Azure deployment target: cluster extensions, custom locations, and Arc data controller connectivity modes."
sources: ["https://learn.microsoft.com/azure/azure-arc/kubernetes/custom-locations", "https://learn.microsoft.com/azure/azure-arc/kubernetes/conceptual-custom-locations", "https://learn.microsoft.com/azure/azure-arc/data/create-data-controller-direct-cli", "https://learn.microsoft.com/azure/azure-arc/data/connectivity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom locations and Arc-enabled data services

**Goal:** let teams deploy Azure services (SQL Managed Instance, App Service, Event Grid etc.) onto your own
Kubernetes as if it were an Azure region (the documentation lists Arc-enabled data services among the offerings).

## Building blocks
Arc-connected cluster -> **cluster extension** (the service's operator in a namespace) -> **custom location**
(an Azure resource mapping to that namespace) -> users deploy resources with `extendedLocation` = the custom location.

## 1. Enable features on the connected cluster
```bash
az connectedk8s enable-features -n arc-k8s-dc1 -g rg-arc --features cluster-connect custom-locations
# if you logged in as a service principal, fetch the Custom Locations service app's object ID and pass it:
#   az ad sp show --id bc313c14-388c-4e7d-a58e-70017303ee3b --query id -o tsv
#   az connectedk8s enable-features ... --custom-locations-oid <oid> --features cluster-connect custom-locations
```
Enable the feature before creating custom locations; register the `Microsoft.ExtendedLocation` provider, and install the `connectedk8s`, `k8s-extension` and `customlocation` CLI extensions.

## 2. Install the extension (example: Arc data services)
The service's operator is installed as a cluster extension before the custom location exists (see the cluster extensions article for `az k8s-extension create`). For Arc data services the direct-mode `az arcdata dc create` command creates the extension, the custom location and the data controller in one step (see section 4), so you only need the manual steps here for other services or custom setups.

## 3. Create the custom location
```bash
EXT_ID=$(az k8s-extension show -c arc-k8s-dc1 -g rg-arc --cluster-type connectedClusters -n arc-data-services --query id -o tsv)
HOST_ID=$(az connectedk8s show -n arc-k8s-dc1 -g rg-arc --query id -o tsv)
az customlocation create -n cl-dc1 -g rg-arc --namespace arc --host-resource-id $HOST_ID --cluster-extension-ids $EXT_ID
```
A custom location maps one-to-one to a namespace; grant teams Azure RBAC on the custom location (deploy rights) rather than on the cluster. `az customlocation update` adds tags or further extension IDs.

## 4. Data controller and SQL MI
- Arc data services supports **direct** connectivity mode only: indirectly connected mode was retired in September 2025. Connections are always initiated from your environment to Azure (HTTPS/443); Entra ID and Azure RBAC, Container Insights and automatic backup to Azure blob storage depend on the direct connection.
- Create the data controller with `az arcdata dc create --name arc-dc1 --resource-group rg-arc --custom-location cl-dc1 --cluster-name arc-k8s-dc1 --connectivity-mode direct --profile-name <profile> --auto-upload-metrics true --auto-upload-logs true --storage-class <class>` (or `--path` to a customised profile directory). Billing and inventory data flow to Azure continuously.

## Gotchas
- Storage classes and capacity are your problem: plan persistent volumes (data, logs, backups) per instance.
- Billing data is sent to Azure automatically in direct mode; check the current Arc data services billing documentation for the meter.

## Verify
- [ ] `az customlocation show` shows provisioningState Succeeded, and the data controller deployed to the custom location reports Ready.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-management-docs `articles/azure-arc` (kubernetes/custom-locations, kubernetes/conceptual-custom-locations, data/create-data-controller-direct-cli, data/connectivity; main branch).
- Confirmed: `az connectedk8s enable-features --features cluster-connect custom-locations`, the service-principal `--custom-locations-oid` flow and the fixed app ID; `az customlocation create` and `update` parameters; one-to-one namespace mapping; extension installed before the custom location; `az arcdata dc create` direct-mode parameters; indirect mode retired in September 2025.
- Removed as unconfirmed: the manual `az k8s-extension create` example for `microsoft.arcdataservices`, the `az sql mi-arc create` command, per-vCore billing and compliance statements, and agent-compatibility advice.
Method: documentation only; no commands were run.
