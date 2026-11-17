---
id: computing-software.cloud-infrastructure-engineering.google-cloud.managing-groups-with-gcloud-identity
name: managing-groups-with-gcloud-identity
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-identity, groups, gcloud-identity-groups, group-membership, dynamic-groups, security-groups, cloud-identity-groups-api, group-based-iam, nested-groups, terraform-google-groups, membership-expiry]
level: practitioner
status: docs-checked
description: "Create and manage Cloud Identity groups and memberships with gcloud identity groups: security groups, dynamic groups and expiring memberships for IAM."
sources: ["https://cloud.google.com/sdk/gcloud/reference/identity/groups", "https://cloud.google.com/identity/docs/how-to/create-dynamic-groups", "https://cloud.google.com/identity/docs/how-to/setup", "https://registry.terraform.io/modules/terraform-google-modules/group/google/latest"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Managing groups with gcloud identity

**Goal:** IAM is granted to groups only, and groups themselves are created, populated and
audited by automation — not by someone with Workspace super-admin clicking in the Admin console.

## 1. Prerequisites
Run the commands as a user who administers groups for the domain; check the gcloud reference for `identity groups` for current
requirements. Commands take `--organization=<DOMAIN>` or `--customer=<CUSTOMER_ID>`.

## 2. Create, find, delete
```bash
gcloud identity groups create gcp-payments-devs@example.com \
  --organization=example.com --display-name="GCP payments developers" --group-type=security
gcloud identity groups describe gcp-payments-devs@example.com
gcloud identity groups search --organization=example.com --labels=cloudidentity.googleapis.com/groups.discussion_forum \
  --format='value(groupKey.id)'
gcloud identity groups delete gcp-payments-devs@example.com
```
`--group-type=security` creates a **security group**, which Google describes as a group used specifically for controlling access
to organisational resources. Use it for IAM groups. (`--group-type` and `--labels` are alternatives in the command synopsis;
`groups search` requires `--labels`.)

## 3. Memberships
```bash
gcloud identity groups memberships add --group-email=gcp-payments-devs@example.com --member-email=alice@example.com
gcloud identity groups memberships add --group-email=... --member-email=bob@example.com --roles=<ROLES>
gcloud identity groups memberships add --group-email=... --member-email=contractor@example.com --expiration=90d
gcloud identity groups memberships delete --group-email=... --member-email=alice@example.com
gcloud identity groups memberships check-transitive-membership --group-email=... --member-email=alice@example.com
```
`--member-email` can be a group or a user. `--expiration` is a duration from now (for example `30d`, `6m`, `3y`), not a timestamp;
expiring memberships are the clean way to grant time-boxed access.

## 4. Dynamic groups
Membership by user attribute query (no manual adds):
```bash
gcloud identity groups create eng-all@example.com --organization=example.com \
  --dynamic-user-query="user.organizations.exists(org, org.department=='engineering')" --group-type=dynamic
```
The flag is `--dynamic-user-query` (there is no `--dynamic-group-query`). Dynamic groups are available only to Google Workspace
Enterprise Standard, Enterprise Plus, Enterprise for Education and Cloud Identity Premium accounts, with up to 500 dynamic groups per customer.

## 5. Naming
Naming: `gcp-<scope>-<role>@` (`gcp-org-admins`, `gcp-prd-payments-devs`) so IAM policies are readable.

## Gotchas
- `identity groups search` requires `--labels`; it does not list "all groups" without one.
- Access changes are eventually consistent.

## Verify
- [ ] `gcloud identity groups describe <group>` shows the group created as a security group.
- [ ] `check-transitive-membership` returns `hasMembership: true` for a nested member.
- [ ] A project IAM policy contains only `group:` and `serviceAccount:` members, no `user:`.

## Checked

- Date: 2026-10-27
- Confirmed against the gcloud references for `identity groups create` (`--organization`/`--customer`, `--group-type` values including security and dynamic, `--dynamic-user-query`, `--labels`), `groups search` (`--labels` required), `memberships add` (`--group-email`, `--member-email`, `--roles`, `--expiration` as a duration such as 30d), `memberships check-transitive-membership`, `memberships delete`, and the Cloud Identity dynamic-groups page (availability by edition, 500-group limit, example query form) and groups overview (security groups).
- Fixed: `--dynamic-group-query` does not exist (it is `--dynamic-user-query`); `--expiration` takes a duration, not an RFC 3339 timestamp; the dynamic-group edition requirement was wrong. Removed: `groups.security` label usage, Terraform resources, admin-console prerequisites, customer-ID lookup command, `memberships list` example, external-member and verified-domain notes and the 7-minute cache claim.

Method: documentation only; no commands were run.
