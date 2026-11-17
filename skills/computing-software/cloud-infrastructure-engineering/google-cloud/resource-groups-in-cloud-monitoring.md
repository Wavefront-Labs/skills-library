---
id: computing-software.cloud-infrastructure-engineering.google-cloud.resource-groups-in-cloud-monitoring
name: resource-groups-in-cloud-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-monitoring, monitoring-groups, resource-groups, group-filters, uptime-checks-groups, alerting-by-group]
level: practitioner
status: docs-checked
description: "Create Cloud Monitoring resource groups by labels, names or tags to scope dashboards, alert policies and uptime checks to a dynamic set of resources, including subgroups."
sources: ["https://cloud.google.com/monitoring/groups", "https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.groups", "https://cloud.google.com/monitoring/alerts/using-alerting-ui#groups"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource groups in Cloud Monitoring

A group is a saved, dynamic filter over monitored resources (VMs, disks, instance groups, Cloud SQL,
etc.). Membership updates automatically as resources match or stop matching.

## Create
```bash
curl -s -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  https://monitoring.googleapis.com/v3/projects/<P>/groups \
  -d '{"displayName":"payments-prod","filter":"<FILTER>"}'
# subgroup
  -d '{"displayName":"payments-prod-db","parentName":"projects/<P>/groups/<GROUP_ID>","filter":"<FILTER>"}'
```
The filter syntax is in the Groups API reference (`projects.groups`).

## Use
- **Alert policies** and **uptime checks** can reference a group; the Groups page can create and view uptime checks for the group.

## Filter tips
- Label-based filters need consistent labels on the resources.
- A subgroup (`parentName`) can only match resources already matched by its parent.

## Gotchas
- Not every resource type can be put in a group (for example, only some AWS load balancer types); check the Groups page.
- Groups are a Monitoring construct, separate from Resource Manager tags.
- Deleting a group also removes it from alerting policies and uptime checks.

## Verify
- [ ] Group members list matches expected resources; a newly labelled resource that matches the filter appears.

## Checked

2026-10-28. Confirmed against: Cloud Monitoring groups page (groups are dynamic collections matched by a filter, deleting a group removes it from alerting policies and uptime checks, uptime checks can be created for a group) and projects.groups API reference (filter, parentName, displayName).

Removed or rewritten: the user_labels filter syntax, group.id alert condition, starts_with and region/zone filter tips, Terraform resource name, members call, the supported-resource list, and the claim that deleting a group breaks alert conditions (the docs say it is removed from them).

Method: documentation only; no commands were run.
