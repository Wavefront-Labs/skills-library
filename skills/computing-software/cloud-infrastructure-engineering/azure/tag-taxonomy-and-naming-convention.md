---
id: computing-software.cloud-infrastructure-engineering.azure.tag-taxonomy-and-naming-convention
name: tag-taxonomy-and-naming-convention
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, tags, tag-taxonomy, naming-convention, naming-standard, resource-naming, caf-naming, abbreviations]
level: practitioner
status: docs-checked
description: "Define an Azure tag taxonomy and resource naming standard from CAF guidance: name components, abbreviations, per-type name rules, tag categories and case rules."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging", "https://learn.microsoft.com/azure/azure-resource-manager/management/resource-name-rules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag taxonomy and naming convention

**Goal:** names that tell an on-call engineer what, which workload, which environment and where, and tags that carry the details that change.

## Naming principles (CAF)
- Most Azure resource names cannot be changed after creation: include only information that stays constant, and use tags for the rest.
- Every name must be unique within its scope (global, resource group, or parent resource), meet length limits and use valid characters, all of which vary by resource type.
- Components to choose from: resource type abbreviation, workload, environment, region, instance number. Fix the component order. A hyphen delimiter helps readability but not every resource allows one.
- Examples from the CAF page: `vm-sql-test-001`, `app-workload1-prod-001`, `vnet-shared-eastus2-001`, `rg-webapp-prod`, `pip-workload4-prod-westus-001`.
- Do not put personal, sensitive or confidential data in names or tags; those fields are not treated as customer data.
- The Azure Naming Tool can generate names from your chosen convention.

## Abbreviations (CAF list)
`rg` resource group, `vnet` virtual network, `snet` subnet, `nsg` network security group, `pip` public IP, `lbe` external and `lbi` internal load balancer, `agw` application gateway, `afd` Front Door, `vm`, `vmss`, `aks`, `cr` container registry, `app` web app, `asp` App Service plan, `func` function app, `kv` key vault, `st` storage account, `sql` SQL server, `sqldb` SQL database, `cosmos` Cosmos DB database, `log` Log Analytics workspace, `appi` Application Insights, `sbns` Service Bus namespace, `evhns` Event Hubs namespace, `evh` event hub, `rsv` Recovery Services vault, `mg` management group.

## Per-type name rules (Resource Manager name rules page)
| Resource | Scope | Length | Characters |
|---|---|---|---|
| Storage account | global | 3-24 | lowercase letters and numbers |
| Key vault | global | 3-24 | alphanumerics and hyphens; start with a letter, end with letter or number, no consecutive hyphens |
| Container registry | global | 5-50 | alphanumerics |
| Virtual machine (Microsoft.Compute) | resource group | 1-15 Windows, 1-64 Linux | no spaces or listed special characters; Windows cannot include periods or end with a hyphen |
| Azure SQL server | global | 1-63 | lowercase letters, numbers, hyphens; not start or end with a hyphen |
| Web app (sites) | global or per domain | 2-60 | alphanumerics, hyphens; not start or end with a hyphen |
| Resource group | subscription | 1-90 | letters, digits, underscore, hyphen, period, parentheses; cannot end with a period |

Storage names have no hyphens, so use a no-delimiter pattern for them (CAF example `stworkload1data001`).

## Tag taxonomy
Tag names (keys) are case insensitive, values are case sensitive: use lowercase keys and consistent value casing, because `Production` and `production` appear separately in cost reports and queries. Tags are plain text and visible in cost reports, API responses, deployment history and exported templates, so never store secrets. Not every resource type supports tags.

CAF foundational categories with its example tags:
| Category | Examples |
|---|---|
| Functional | app, tier, env, region |
| Classification | criticality, confidentiality, sla |
| Accounting | department, program, costcenter |
| Purpose | businessprocess, businessimpact, revenueimpact |
| Ownership | businessunit, opsteam |

Define which tags are mandatory and which optional. Enforce with Azure Policy built-in and custom definitions (assignment resource selectors such as `resourceLocation` can target regions). For chargeback beyond subscription level see tag inheritance in Cost Management.

## Checked
Confirmed against the four cited Microsoft Learn pages (naming last updated 2026-06-25, tagging 2025-07-01, abbreviations and name rules as fetched), 2026-11-08. Corrected: `acr` is `cr`, `law` is `log`, `lb` is `lbe`/`lbi`, a Windows VM resource name is 1-15 characters (not just the computer name). Removed: the custom naming pattern with region codes, Key Vault soft-delete name reservation, Bicep `take()`/`uniqueString()` snippet, the tag table with Deny enforcement, "5-8 mandatory tags", Terraform naming module, what-if and Resource Graph checks, the 98% compliance target and managed resource group advice, because the pages do not state them.
Method: docs-only read of cited pages, 2026-11-08
