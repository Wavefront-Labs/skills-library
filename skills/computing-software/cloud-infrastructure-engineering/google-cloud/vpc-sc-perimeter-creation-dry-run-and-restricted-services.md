---
id: computing-software.cloud-infrastructure-engineering.google-cloud.vpc-sc-perimeter-creation-dry-run-and-restricted-services
name: vpc-sc-perimeter-creation-dry-run-and-restricted-services
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-service-controls, perimeter-creation, gcloud-access-context-manager-perimeters, vpc-sc-dry-run, perimeter-dry-run, restricted-services, vpc-accessible-services]
level: advanced
status: docs-checked
description: "Create VPC Service Controls perimeters with gcloud: choose restricted and VPC-accessible services, roll out in dry-run, read dry-run violations, then enforce without outages."
sources: ["https://cloud.google.com/vpc-service-controls/docs/create-service-perimeters", "https://cloud.google.com/vpc-service-controls/docs/dry-run-mode", "https://cloud.google.com/vpc-service-controls/docs/vpc-accessible-services", "https://cloud.google.com/sdk/gcloud/reference/access-context-manager/perimeters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC-SC: perimeter creation, dry-run and restricted services

## 1. Policy and perimeter
```bash
POLICY=$(gcloud access-context-manager policies list --organization=<ORG_ID> --format='value(name)')
# start as DRY-RUN only (no enforcement)
gcloud access-context-manager perimeters dry-run create data-prod --policy=$POLICY \
  --perimeter-title="data prod" --perimeter-type=regular \
  --perimeter-resources=projects/<NUM1>,projects/<NUM2> \
  --perimeter-restricted-services=storage.googleapis.com,bigquery.googleapis.com,secretmanager.googleapis.com \
  --perimeter-enable-vpc-accessible-services --perimeter-vpc-allowed-services=RESTRICTED-SERVICES
```
Resources are **project numbers** (`projects/<NUMBER>`; names and IDs are not accepted) or VPC network names, and a perimeter cannot contain projects from different organizations. Restrict every service that holds or moves your data.
VPC accessible services limit which APIs the perimeter's VPC networks can reach; the value `RESTRICTED-SERVICES` includes every service the perimeter protects. In the console, a perimeter name is limited to 50 characters (ASCII letters, digits, underscores, starting with a letter) and must be unique within the access policy.

## 2. Read dry-run violations
```
protoPayload.metadata.dryRun=true
```
In dry-run audit logs the `metadata.dryRun` field is true. Dry run logs a request only if enforced mode did not already deny it and it violates the dry-run configuration. Group by caller identity and service. Each violation is either an
expected block (good), or a legitimate flow needing an ingress/egress rule or access level.
Leave dry-run running through at least one full business cycle (month-end jobs!).

## 3. Enforce
```bash
gcloud access-context-manager perimeters dry-run enforce data-prod --policy=$POLICY   # copies dry-run config to enforced
gcloud access-context-manager perimeters describe data-prod --policy=$POLICY
```
`dry-run enforce` copies the dry-run configuration to the enforcement configuration and unsets the explicit dry-run spec; it fails if there is no explicit dry-run configuration. For later changes, modify the dry-run configuration first, observe the logs, then enforce again.

## Gotchas
- A new or changed perimeter can take up to 30 minutes to propagate, and during that time may block requests with "Error 403: Request is prohibited by organization's policy".
- A project can be in only one enforced and one dry-run configuration (not necessarily the same perimeter), so moving a project between perimeters must be sequenced.
- Dry run does not show the impact of moving traffic to the restricted or private VIP; check that all services you use are available on the restricted VIP before configuring `restricted.googleapis.com`.
- VPC accessible services only apply to traffic from VPC network endpoints to Google APIs; services not in the allowed list are not reachable from those networks.

## Verify
- [ ] Dry-run violation count trends to only expected blocks before enforcement.
- [ ] After enforcement, requests from outside the perimeter to protected services are denied and in-perimeter workloads run normally.

## Checked
2026-10-27. Confirmed against the VPC Service Controls Create a service perimeter, Dry run mode and VPC accessible services pages and the gcloud perimeters dry-run create and dry-run enforce reference pages (flags, --policy, project-number resource format, RESTRICTED-SERVICES value, metadata.dryRun, enforce semantics, 30-minute propagation, one enforced and one dry-run configuration per project). Removed: the config-set policy property (replaced by --policy), scoped-policies advice, the @type and violationReason log fields, instant-enforcement and Google-managed-service violation claims, the oslogin example, bq ls verify step. Method note: the dry-run update subcommand was not fetched, so later changes are described generically.
Method: documentation only; no commands were run.
