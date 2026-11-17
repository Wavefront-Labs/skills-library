---
id: computing-software.cloud-infrastructure-engineering.rancher.hosted-aks-cluster-service-principal
name: hosted-aks-cluster-service-principal
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [aks, azure, service-principal, contributor, subscription-id, hosted-clusters]
level: practitioner
status: docs-checked
description: "Prepare Azure for Rancher-created AKS clusters: Contributor service principal, subscription ID, client ID and secret, resource group."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-clusters-in-rancher-setup/set-up-clusters-from-hosted-kubernetes-providers/aks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To create AKS clusters Rancher needs a Microsoft Entra ID **service principal**, which dynamically creates and manages Azure resources and gives the cluster credentials to talk to AKS. Deploying to AKS incurs charges.

Collect three values from the Azure Portal: **Subscription ID**, **Client ID** (app ID) and **Client secret**.

With the Azure CLI, create the principal with the Contributor role. Contributor can manage anything on AKS but cannot grant access to others. The `scopes` value must be a full path to at least one Azure resource:

```
az ad sp create-for-rbac --role Contributor --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group-name>
```

The output includes `appId`, `password` (the secret) and `tenant`. Create a resource group to hold the resources:

```
az group create --location <azure-location-name> --resource-group <resource-group-name>
```

Through the portal instead: **Microsoft Entra ID > App registrations > New registration**, note the application (client) ID, then **Certificates & secrets > New client secret** and record the secret before it is hidden. A new service principal still needs role-based access: go to **Subscriptions**, open the subscription, and assign a role to it.

The service principal needs roles that let it communicate with the AKS API and create and list virtual networks.

## Checked

2026-11-09. Read the cited Creating an AKS Cluster page in full and checked every claim against it (service principal purpose, three values, az ad sp create-for-rbac and az group create commands, portal steps, role assignment). Renamed Azure Active Directory to Microsoft Entra ID as the page does. Removed the claim that Entra ID-authenticated AKS clusters cannot be imported, which the page does not state.

Method: documentation only; no commands were run.
