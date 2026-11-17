---
id: computing-software.systems-network-administration.patch-management.asset-ownership-and-tagging
name: asset-ownership-and-tagging
category: computing-software
field: systems-network-administration
product: patch-management
tags: [asset-owner, asset-tagging, cmdb, patch-management, accountability]
level: practitioner
status: docs-checked
description: "Assign and enforce technical and business owners on every asset via CMDB fields and cloud tags so patch findings route to someone accountable, with orphan reports."
sources:
  - https://learn.microsoft.com/en-us/azure/governance/policy/samples/built-in-policies#tags
  - https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html
  - https://www.cisecurity.org/controls/inventory-and-control-of-enterprise-assets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asset ownership and tagging

**Goal:** every server, endpoint group, cloud resource and container workload has a named
owner, so a patch finding becomes a ticket in someone's queue on day one. CIS Control 1
frames this as actively managing all enterprise assets so you know the totality of what
needs to be monitored and protected, and can spot unauthorised and unmanaged assets.

## Two owners
- **Technical owner** (team or queue): patches, reboots, fixes. Use a group, not a person
  who might leave.
- **Business/application owner**: accepts risk, signs off downtime and exceptions.
Record both, plus environment, criticality and patch group.

## Tag standard (cloud)
Tags are key/value pairs; AWS says tags can categorise resources by purpose, owner or
environment. AWS tag keys and values are case sensitive, so pick one spelling and avoid
keys that differ only in case. Do not put PII or other sensitive data in tags. Example
keys: `owner-team`, `app`, `env`, `criticality`, `patch-group`.

Ways to apply AWS tags: a service's own API, the Tag Editor console, or the Resource
Groups Tagging API (most services).

Enforce at creation in Azure with built-in policies listed under "Tags" in the Azure
Policy built-in definitions: "Require a tag on resources", "Require a tag and its value",
"Inherit a tag from the resource group" and "Add a tag to resources".

## On-prem
Keep owner fields on the CMDB configuration item and populate them from discovery or
reconciliation, so that on-prem assets are as routable as cloud ones.

## Orphan report
Run a regular report of assets with no owner value, route it to the infrastructure
manager with a deadline, and define in advance what happens to assets that stay unowned.

## Gotchas
- Free-text owner names rot; validate against a list of real groups.
- Reorganisations break ownership silently, so re-confirm owners on a schedule.

## Verify
Patch findings report: no open finding lacks a routable owner; orphan count trends to
zero.

## Checked
2026-11-08. Confirmed against the AWS Tag Editor user guide (tag definition, case
sensitivity, PII warning, three tagging methods), the Azure Policy built-in definitions
page (the four tag policy names) and the CIS Control 1 overview. Removed claims the pages do
not support: AWS Organizations tag policies and SCP example, Kyverno/Gatekeeper, the AD
`managedBy` attribute and CMDB field names, the PowerShell and AWS CLI orphan queries, and
the 14-day deadline.
Method: documentation only; no commands were run.
