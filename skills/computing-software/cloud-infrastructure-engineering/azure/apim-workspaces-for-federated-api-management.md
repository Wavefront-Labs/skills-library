---
id: computing-software.cloud-infrastructure-engineering.azure.apim-workspaces-for-federated-api-management
name: apim-workspaces-for-federated-api-management
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, api-management, apim-workspaces, federated-api-management, workspace-gateway]
level: advanced
status: docs-checked
description: "Use API Management workspaces so product teams own their APIs in one APIM instance: workspace gateways, RBAC roles, and policy scopes."
sources: ["https://learn.microsoft.com/azure/api-management/workspaces-overview", "https://learn.microsoft.com/azure/api-management/how-to-create-workspace", "https://learn.microsoft.com/azure/api-management/api-management-role-based-access-control"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APIM workspaces for federated API management

**Goal:** let many teams publish APIs independently while a platform team runs one governed APIM instance.

## Model
- **Workspace**: a container for one team's APIs and related entities, managed by that team with segregated administrative permissions; the platform team keeps central governance, monitoring and API discovery, with a unified developer portal.
- Availability: workspaces are available in the Basic v2, Standard v2, Premium and Premium v2 tiers.
- **Gateways**: a workspace runs on the service's default managed gateway (currently in the v2 tiers; shared capacity and configuration, no extra cost, supports multi-region deployments, custom hostnames and private link where the tier does) and/or on one or more **workspace gateways** (Premium and Premium v2: separate gateway resources with runtime isolation, independent scaling, hostname and network configuration, extra cost, longer deployment, fewer regions).
- Workspace gateways can be placed in a private virtual network with a dedicated subnet; see the network requirements article.

## Create and delegate
Create the workspace in the portal (see "Create a workspace in API Management"), associate it with a gateway, and assign roles.

A workspace collaborator needs **both** a workspace-scoped role and a service-scoped role:
| Role | Scope | Purpose |
|---|---|---|
| API Management Workspace Contributor / Reader | workspace | manage / read workspace entities |
| API Management Workspace API Developer | workspace | read, plus edit APIs |
| API Management Workspace API Product Manager | workspace | read, plus publish APIs |
| API Management Service Workspace API Developer | service | read tags and products; assign APIs and tags to products |
| API Management Service Workspace API Product Manager | service | same as the developer role plus read users and assign users to groups |
If the workspace uses a workspace gateway resource, also assign Reader, Contributor or Owner on that gateway resource.

## Policy scopes
Policies can be defined at global, workspace, product, API and operation scopes. A built-in Azure Policy definition (`API Management policies should inherit parent scope policies using <base/>`) audits or enforces that workspace policies inherit parent scope policies.

## Verify
- [ ] A team member with only the workspace and service workspace roles can publish an API in their workspace and cannot edit another workspace.
- [ ] Calls through the workspace's gateway succeed and appear in the team's monitoring.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (api-management: workspaces-overview, how-to-create-workspace, api-management-role-based-access-control, llm-emit-token-metric-policy for the scope list): tier availability (Basic v2, Standard v2, Premium, Premium v2), default managed gateway versus workspace gateway comparison, network isolation, built-in workspace and service workspace roles and their scopes and descriptions, requirement of both a workspace and a service role, the base-inheritance Azure Policy definition. Removed the unconfirmed Bicep resource type and API version, the Microsoft.ApiManagement/gateways and configConnections statement, the policy execution order and the feature-gap and network remarks.

Method: documentation only; no commands were run.
