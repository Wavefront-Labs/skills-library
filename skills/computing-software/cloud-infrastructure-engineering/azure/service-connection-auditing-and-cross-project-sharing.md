---
id: computing-software.cloud-infrastructure-engineering.azure.service-connection-auditing-and-cross-project-sharing
name: service-connection-auditing-and-cross-project-sharing
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, pipeline-secrets, service-connection-audit, service-connection-sharing, workload-identity-federation, approvals-checks]
level: advanced
status: docs-checked
description: "Govern Azure DevOps service connections: audit usage, restrict pipeline permissions, add approvals and checks, and move to workload identity federation on the Entra issuer."
sources: ["https://learn.microsoft.com/azure/devops/pipelines/library/service-endpoints", "https://learn.microsoft.com/azure/devops/organizations/audit/azure-devops-auditing", "https://learn.microsoft.com/azure/devops/pipelines/release/configure-workload-identity", "https://learn.microsoft.com/azure/devops/pipelines/security/resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service connection governance

**Goal:** know who can deploy where with which identity, and limit blast radius.

## Inventory and audit
```bash
az devops service-endpoint list --org https://dev.azure.com/<org> -p <project> \
  --query "[].{name:name, type:type, scheme:authorization.scheme, shared:isShared, ready:isReady}" -o table
```
- Prefer workload identity federation (app registration or managed identity), which removes secrets from the connection.
- Each connection has a **Usage history** tab showing historical usage.
- **Auditing** is under Organization settings. Access needs Project Collection Administrators membership, or the
  auditing permissions (View audit log, Manage audit streams) granted to a user or group. If Auditing doesn't appear,
  you lack access.
- Map each connection to its Azure identity and role assignments in Azure (`az role assignment list --assignee <appId> --all`).

## Workload identity federation: issuer change
Connections that use the Azure DevOps issuer (`https://vstoken.dev.azure.com`) are deprecated and retire on
1 July 2027; new connections use the Microsoft Entra issuer (`https://login.microsoftonline.com/`) by default. Flagged
connections show in the list; select **Update** to convert, or add the federated credential manually if you lack identity access.
Azure DevOps and Azure/Entra permissions are separate: you may need an identity owner to add the federated credential.

## Restrict use
- Don't select **Grant access permission to all pipelines**; authorize each pipeline individually.
- Don't enable Open access on protected resources (all pipelines in the project could use them); enabling access for
  all pipelines needs the Project Administrator role.
- Members of the **User** role on a resource can manage its approvals and checks: grant it sparingly.
- Checks on a connection: branch control (only authorised branches), business hours, required templates, approvals.
- Service connection administrators and Project Administrators can **Disable** an unused connection; pipelines that
  reference it fail or are denied until it is enabled again.
- Scope the Azure identity narrowly (a resource group role rather than subscription Owner).

## Verify
- [ ] Report lists every connection with owner, identity, roles, scheme and last use; no secret-based connections remain; prod connections have branch control checks.

## Checked
2026-10-31. Confirmed against Learn "Service connections", "Azure DevOps auditing", "Configure workload identity
federation" and "Secure access to resources": Usage history, auditing access, issuer deprecation and 1 July 2027 date,
Update/convert flow, all-pipelines option, Open access, User role, branch control and business hours checks, Disable.
Removed: audit event names, project-sharing steps and the job authorization scope setting (not on the pages read),
the per-role Administrator/User/Reader list, exclusive lock check, and the `Edit -> Convert` UI path.
Method: documentation only; no commands were run.
