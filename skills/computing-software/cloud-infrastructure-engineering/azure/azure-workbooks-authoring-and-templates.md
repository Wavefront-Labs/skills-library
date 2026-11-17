---
id: computing-software.cloud-infrastructure-engineering.azure.azure-workbooks-authoring-and-templates
name: azure-workbooks-authoring-and-templates
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor, workbooks, workbooks-authoring, workbook-templates, kql, parameters, dashboards, gallery-templates, log-analytics]
level: practitioner
status: docs-checked
description: "Author Azure Monitor workbooks: parameters, KQL steps, global parameters and tabs, then export as gallery templates or ARM resources."
sources: ["https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-overview", "https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-parameters", "https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-automate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Monitor workbooks: author once, deploy as code

**Goal:** an interactive report that people pick a time range or resource in and drill through, version-controlled and deployed like any other resource.

## 1. What a workbook is
Workbooks combine text, log queries, metrics and parameters into interactive reports, and can query data from multiple Azure sources, including composite views and joins across resources. The gallery has four tabs: All, Workbooks (yours or shared with you), Public Templates (published by Microsoft) and My Templates (deployed templates you created or that are shared with you).

## 2. Parameters drive everything
- Reference a parameter in KQL by name in braces. For a time range parameter, `| where timestamp {TimeRange}` expands at evaluation time to a condition such as `| where timestamp > ago(1d)`.
- In text steps use a format option, for example `{TimeRange:label}` renders "Last 24 hours".
- Formatting options include `{param:escapejson}`, `{param:base64}` and `{param:tomltojson}`; for JSON string parameters use JSONPath such as `{selection:$.series}` (an invalid JSON value gives an empty result). The Previews section of the Edit Parameter pane shows the expansion options per type.
- Parameter styles: Pills (default), Standard, Form horizontal, Form vertical.
- A parameter can normally only be used downstream of where it is set. A **global parameter** (Advanced Settings, "Treat this parameter as a global") lifts that: it must still be declared in a parameters step, but selections, brushing, links, buttons and tabs can update it. Typical uses are syncing a time range across charts (with time brushing and "Only export the parameter when a range is brushed") and a global `selectedTab` driving a links-step tab set.

## 3. Access
Permissions follow the permissions the user has on the resources in the workbook. Monitoring Reader covers reads; Monitoring Contributor includes `workbooks/write` for saving shared workbooks. Custom roles need `microsoft.insights/workbooks/write` to edit and save.

## 4. Deploy as code
- Open the **Advanced Editor** (the `</>` toolbar button), stay on the **Gallery Template** tab and copy the JSON.
- Put that JSON into an ARM template resource of type `microsoft.insights/workbooktemplates` to publish a gallery template.
- A workbook instance is deployed with an ARM template whose workbook resource carries the content in the `serializedData` parameter and a unique GUID for the instance (the Learn example defaults it to `[newGuid()]`).
- Exported `serializedData` can embed fixed resource links including subscription ID and resource group, so review it before committing.

## Gotchas
- Without a global parameter, a time range brushed in one chart only affects steps below it.

## Verify
- [ ] Changing the time range or resource selection updates every step that should depend on it.
- [ ] The exported JSON in Git deploys via pipeline and the result matches the authored workbook.

## Checked
Method: docs-checked 2026-11-09 against workbooks-overview, workbooks-parameters and workbooks-automate (downloaded with curl; structure, access control, parameter formatting, global parameters and ARM template sections read). Dropped step-type tables, the Bicep resource and API version, the RBAC role names beyond Monitoring Reader/Contributor, and the unconfirmed grain and My reports claims.
