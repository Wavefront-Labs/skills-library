---
id: computing-software.cloud-infrastructure-engineering.azure.abac-custom-security-attributes-as-principal-attributes
name: abac-custom-security-attributes-as-principal-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, abac, custom-security-attributes, principal-attributes, entra-id, attribute-sets, role-assignment-conditions]
level: advanced
status: docs-checked
description: "Use Entra custom security attributes as @Principal attributes in Azure ABAC conditions so one role assignment scales across projects without per-team assignments."
sources: ["https://learn.microsoft.com/entra/fundamentals/custom-security-attributes-overview", "https://learn.microsoft.com/azure/role-based-access-control/conditions-custom-security-attributes", "https://learn.microsoft.com/entra/fundamentals/custom-security-attributes-add", "https://learn.microsoft.com/azure/role-based-access-control/conditions-format#principal-attributes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom security attributes as principal attributes in ABAC

**Goal:** a single role assignment such as "Storage Blob Data Reader for group *Analysts*" that
lets each analyst read only blobs whose `Project` index tag matches the `Project` attribute on
their own user object.

## 1. Roles needed
- **Attribute Definition Administrator** — create attribute sets and definitions.
- **Attribute Assignment Administrator** — set values on users/service principals.
- **Attribute Definition Reader/Assignment Reader** for people who author conditions.

## 2. Define the attribute
Entra admin center → Entra ID → Custom security attributes → **Add attribute set**
`Engineering` (max 500 sets per tenant) → **Add attribute** `Project`, type String,
*Allow multiple values* yes, *Only predefined values* yes (values `Alpine`, `Baker`, `Cascade`).
Attribute sets cannot be renamed or deleted, and a definition can be deactivated but not deleted. The Microsoft Graph
`customSecurityAttributeDefinition` API does the same as code (see its reference page).

## 3. Assign values to principals
Set values in the portal (user → Custom security attributes → Add assignment) or with the Graph `customSecurityAttributes`
property on the user or service principal (see the Graph reference); for this example set `Engineering_Project` to `Baker` and `Cascade`.

## 4. Write the condition
```
(
 (!(ActionMatches{'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read'}
   AND NOT SubOperationMatches{'Blob.List'}))
 OR
 (@Principal[Microsoft.Directory/CustomSecurityAttributes/Id:Engineering_Project]
   ForAnyOfAnyValues:StringEquals
  @Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs/tags:Project<$key_case_sensitive$>])
)
```
Assign `Storage Blob Data Reader` to the Analysts group with this condition, version 2.0.
Now onboarding to a project is an attribute change, not a new role assignment.

## Gotchas
- Attribute values are case-sensitive in comparisons; predefined values prevent typos.
- Attribute definitions can't be deleted, only deactivated.
- Blob listing does not filter by tag; users see names they can't read. Use separate prefixes if names are sensitive.

## Verify
- [ ] `GET /users/<id>?$select=customSecurityAttributes` returns the expected Project values.
- [ ] User with `Project=Baker` reads a blob tagged `Project=Baker` and is denied on `Project=Alpine`.
- [ ] Role assignment list shows a single assignment with `conditionVersion: 2.0`.

## Checked
2026-10-27. Confirmed on Microsoft Learn: custom-security-attributes-overview (Attribute Definition Administrator, Attribute Assignment Administrator, Definition Reader and Assignment Reader roles; 500 attribute sets per tenant),
custom-security-attributes-add (Entra ID > Custom security attributes, Add attribute set, Allow multiple values, predefined values, sets cannot be renamed or deleted, definitions can be deactivated not deleted),
conditions-custom-security-attributes and conditions-format (`@Principal[Microsoft.Directory/CustomSecurityAttributes/Id:Engineering_Project]`, `SubOperationMatches{'Blob.List'}`, `ForAnyOfAnyValues`).
Removed: Graph request bodies (Graph endpoints could not be read without a token), "cannot be set on groups", propagation-delay, deactivated-attribute and guest statements, Global Admin note, scope advice.

Method: documentation only; no commands were run.
