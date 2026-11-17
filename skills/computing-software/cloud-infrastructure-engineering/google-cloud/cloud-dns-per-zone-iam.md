---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-dns-per-zone-iam
name: cloud-dns-per-zone-iam
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-dns, dns-zone-iam, per-zone-iam, least-privilege, shared-vpc]
level: practitioner
status: docs-checked
description: "Delegate control of individual Cloud DNS managed zones with zone-level IAM, so teams edit their own zone without project-wide dns.admin, including cross-project binding."
sources: ["https://cloud.google.com/dns/docs/zones/iam-per-resource-zones", "https://cloud.google.com/dns/docs/access-control", "https://cloud.google.com/sdk/gcloud/reference/dns/managed-zones", "https://cloud.google.com/dns/docs/zones/cross-project-binding"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud DNS per-zone IAM

## 1. Grant on a zone
```bash
gcloud dns managed-zones get-iam-policy team-a-zone --project=DNS_PROJECT_ID > policy.yaml
# edit policy.yaml: add a binding for group:team-a@example.com with role roles/dns.admin
gcloud dns managed-zones set-iam-policy team-a-zone policy.yaml --project=DNS_PROJECT_ID
```
The `managed-zones` group has `get-iam-policy` and `set-iam-policy` only (no add-iam-policy-binding). Needed permissions: `dns.managedZones.setIamPolicy` and `getIamPolicy` (held by `roles/iam.securityAdmin` and `roles/dns.admin`). Roles: `roles/dns.reader`, `roles/dns.admin`, and `roles/dns.peer` for peering targets.
For finer control, IAM Conditions on `dns.googleapis.com/ResourceRecordSet` resources can limit which record sets a principal manages (the condition must also allow `dns.googleapis.com/Change`); or split delegated subdomains into their own zones (`team-a.example.com.`) and add NS records in the parent.

## 2. Pattern for central DNS projects
- Central networking team owns the DNS project and parent zones with project-level `dns.admin`.
- Each app team gets zone-level `dns.admin` on its subdomain zone only.
- CI service accounts get zone-level grants used by Terraform/ExternalDNS.

## 3. Private zones and Shared VPC
Private zones bound to the host VPC live in the host project; grant service-project teams zone-level
admin on their private zone rather than DNS admin on the host project. Cross-project binding
(`--networks` from another project in the same organization) needs `dns.networks.bindPrivateDNSZone` on the project that owns the network and `dns.managedZones.create` on the zone's project.

## Gotchas
- Cloud DNS supports IAM at project level (the default) and individual zone level; review project-level `dns.admin` grants so zone grants are meaningful.
- `dns.managedZones.list` is needed to test IAM permissions on a zone.

## Verify
- [ ] A team member can create records in their zone and gets PERMISSION_DENIED on a sibling zone.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: `gcloud dns managed-zones add-iam-policy-binding` does not exist (its reference page returns 404; the managed-zones group lists only get-iam-policy and set-iam-policy), so the grant is now done by editing and setting the policy file. Found stale: 'no record-level IAM' (the per-zone IAM page documents IAM Conditions on resource record sets).
- Confirmed (per-zone IAM page): dns.managedZones.setIamPolicy, getIamPolicy and list permissions, roles/iam.securityAdmin and roles/dns.admin can set policy. Confirmed (access control page): roles dns.admin, dns.reader and dns.peer; IAM at project and zone level; dns.networks.bindPrivateDNSZone needed on projects with authorised VPC networks.
- Confirmed (cross-project binding page): same-organization limitation and the two permissions.
- Removed: the console-listing note and the claim that deleting a zone drops its IAM policy (not found in documentation).

Method: documentation only; no commands were run.
