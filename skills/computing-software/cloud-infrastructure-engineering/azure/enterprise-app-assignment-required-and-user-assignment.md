---
id: computing-software.cloud-infrastructure-engineering.azure.enterprise-app-assignment-required-and-user-assignment
name: enterprise-app-assignment-required-and-user-assignment
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, enterprise-apps, assignment-required, user-assignment, app-role-assignment]
level: practitioner
status: docs-checked
description: "Restrict who can sign in to an Entra enterprise app: assignment required, user/group app role assignments, client-app assignments via Graph, and consent effects."
sources: ["https://learn.microsoft.com/entra/identity/enterprise-apps/assign-user-or-group-access-portal", "https://learn.microsoft.com/entra/identity-platform/howto-restrict-your-app-to-a-set-of-users", "https://learn.microsoft.com/graph/api/serviceprincipal-post-approleassignedto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assignment required and user assignment

**Goal:** only intended users (and apps) can get tokens for an application. By default an app registered in a tenant is available to all users of that tenant who authenticate successfully.

## Turn it on
Entra ID > Enterprise apps > All applications > the app > Properties > **Assignment required?** = Yes > Save. You must be the app owner or at least a Cloud Application Administrator. It works for SAML single sign-on apps, Application Proxy apps with Entra preauthentication, and OAuth 2.0/OpenID Connect apps built on the Entra platform after consent.

With Graph PowerShell: `Update-MgServicePrincipal -ServicePrincipalId <id> -AppRoleAssignmentRequired:$true`.

## Assign users and groups
Enterprise apps > the app > Users and groups > Add user/group > select principals > Select a role (the default is **Default Access** when no roles are defined) > Assign. Roles needed: Cloud Application Administrator, Application Administrator, User Administrator, or owner of the service principal.

- Group-based assignment requires Microsoft Entra ID P1 or P2. Assignment does not cascade to nested groups, and nested group membership is not currently supported.
- Graph request (permissions `Application.ReadWrite.All` and `AppRoleAssignment.ReadWrite.All` in Graph Explorer): `POST https://graph.microsoft.com/v1.0/servicePrincipals/{resource-sp-id}/appRoleAssignedTo` with body `principalId`, `resourceId` (the enterprise app service principal id) and `appRoleId`. The default role id is `00000000-0000-0000-0000-000000000000`. Success returns 201 Created.
- Unassign: `GET .../appRoleAssignedTo` to find the assignment id, then `DELETE .../appRoleAssignedTo/{appRoleAssignment-id}`; Graph Explorer has no batch delete.

## Client apps (app-to-app)
To restrict a resource app to specific services, find them in Service Principal sign-in logs, make sure service principals exist for both resource and client apps (`New-MgServicePrincipal -AppId`), then assign the client service principal to the resource with `New-MgServicePrincipalAppRoleAssignment`. This explicit client assignment is available only through the API, not the Entra admin center. Then set assignment required on the resource.

## Consent effect
When an app requires assignment, user consent for it is not allowed, even if user consent would otherwise be permitted. Grant tenant-wide admin consent first.

## Gotchas
- Global Administrators are not subject to the user assignment requirement.
- Turning assignment on for an app already in use blocks anyone not assigned: assign groups first and check sign-in logs.
- To block an app entirely, create a service principal for it and disable user sign-in.

## Checked
Confirmed against the three cited Microsoft Learn pages (assign users and groups, restrict an app to a set of users, Graph appRoleAssignedTo POST), 2026-11-08. Removed: the `az ad sp update` and `az rest` commands, the AADSTS50105 text, the "Visible to users?" setting, first-party app limits, dynamic group and access package advice, and the claim that admin-consented application permissions create the assignment, because the pages do not state them.
Method: docs-only read of cited pages, 2026-11-08
