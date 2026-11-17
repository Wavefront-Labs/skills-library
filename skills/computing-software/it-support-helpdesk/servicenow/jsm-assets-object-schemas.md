---
id: computing-software.it-support-helpdesk.servicenow.jsm-assets-object-schemas
name: jsm-assets-object-schemas
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, jira-service-management, jsm, jsm-assets, assets-schema, aql, cmdb, assets-custom-field]
level: practitioner
status: draft
description: "Use Jira Service Management Assets for support: object schemas and types, attributes and references, AQL, Assets fields on request types, and importing devices."
sources:
  - "https://support.atlassian.com/jira-service-management-cloud/docs/what-is-assets/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/use-assets-query-language-aql/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/import-data-to-assets/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jsm-assets-object-schemas

Assets (formerly Insight) is JSM's CMDB/asset database. Support uses it so a request
shows *which laptop*, routing can depend on the service, and agents see history per device.

## Model
- **Object schema**: a container (e.g. "IT Assets", "Services").
- **Object type**: Laptop, Monitor, Mobile phone, Application service, Employee.
  Inheritance lets Laptop and Desktop share Hardware attributes.
- **Attributes**: text, date, status, user, and **object references** (Laptop "Owner" ->
  Employee; Application "Depends on" -> Server). References power impact views.
- Statuses per object type (In use, In stock, Repair, Retired).

## AQL essentials
```
objectType = Laptop AND Owner = currentReporter()
objectType = Laptop AND Status = "In stock" AND Model LIKE "Latitude"
objectType = "Application service" AND "Support team" = "Desktop"
Owner.Department = Finance
```
Use AQL in the Assets custom field filter, Assets searches, and automation lookups.

## Request types
1. Create an **Assets object** custom field (Cloud) with filter scope AQL e.g.
   `objectType = Laptop` and filter issue scope `Owner = ${reporter}` so customers only
   see their own devices.
2. Add it to the request type form ("Which device?") and the agent view.
3. Automation: "Lookup objects" action with AQL, then set fields (e.g. assign to the
   support team from the related service) or comment with warranty date.

## Getting data in
- Imports: CSV, JSON, database, and Assets Discovery; mapping per object type with an
  identifier attribute (serial number) to update rather than duplicate.
- Integrations/adapters for Intune, Jamf, and cloud providers exist in the Atlassian
  Marketplace and as native integrations; schedule nightly syncs.

## Gotchas
- Missing identifier mapping on import creates duplicates every run.
- Customers can only select objects if the field's issue scope and their permissions
  allow; "no options" on the portal usually means the AQL references a field the
  customer lacks.
- Object-level permissions: schema roles (Object schema users / managers); agents need at
  least Object viewers.

## Verify
On the portal, a test user sees only their devices; selecting one shows it on the agent
view; nightly import updates existing objects (count stable) and adds new ones.
