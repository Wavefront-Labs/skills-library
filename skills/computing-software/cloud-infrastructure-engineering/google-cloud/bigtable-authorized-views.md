---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigtable-authorized-views
name: bigtable-authorized-views
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigtable, bigtable-authorized-views, iam, multi-tenant, data-sharing]
level: advanced
status: docs-checked
description: "Share a subset of a Bigtable table with authorized views: row-prefix and column-family/qualifier filters, view-level IAM, and reading or writing through the view."
sources: ["https://docs.cloud.google.com/bigtable/docs/authorized-views", "https://docs.cloud.google.com/sdk/gcloud/reference/bigtable/authorized-views/create", "https://github.com/googleapis/googleapis/blob/master/google/bigtable/admin/v2/table.proto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bigtable authorized views

An authorized view is a named subset of a table (row-key prefixes and/or column families/qualifiers)
with its own IAM policy. Use it for per-tenant access on a shared table, or to hide sensitive columns.

## 1. Define the view
`view.json`:
```json
{"subsetView": {
  "rowPrefixes": ["dGVuYW50QSM="],
  "familySubsets": {"profile": {"qualifiers": ["bmFtZQ==", "cGxhbg=="]}, "events": {"qualifierPrefixes": [""]}}
}}
```
Prefixes and qualifiers are base64 by default (`tenantA#`, `name`, `plan`); pass `--pre-encoded` if they are already encoded. An empty qualifier prefix means the whole family, and an empty row prefix gives access to all rows. The definition file may be JSON or YAML and may also carry `"deletionProtection": true`. A view allows at most 10 distinct qualifier prefixes.
```bash
gcloud bigtable authorized-views create tenantA --instance=<I> --table=accounts --definition-file=view.json
gcloud bigtable authorized-views describe tenantA --instance=<I> --table=accounts
```

## 2. Grant on the view, not the table
```bash
gcloud bigtable authorized-views add-iam-policy-binding tenantA --instance=<I> --table=accounts \
  --member=serviceAccount:tenant-a@<P>.iam.gserviceaccount.com --role=roles/bigtable.reader
```
The view resource name is `projects/<P>/instances/<I>/tables/accounts/authorizedViews/tenantA`. A view controls both read and write access to the subset it defines.

## Gotchas
- A principal with table- or instance-level `bigtable.reader` sees everything: audit that no broader grant exists.
- Check the Bigtable authorized-views documentation for the current list of operations and client features supported through a view.
- `deletionProtection` on a view protects it against deletion; while any view has it set, the parent table and instance cannot be deleted.

## Verify
- [ ] Reading a row of another tenant through the view returns nothing, and writes outside the view are not accepted.

## Checked
Checked 2026-10-24 against the googleapis `google/bigtable/admin/v2/table.proto` (AuthorizedView, SubsetView, FamilySubsets, deletion_protection), the gcloud `bigtable authorized-views create` reference and the authorized views overview (docs.cloud.google.com). Confirmed the definition-file fields, base64 and `--pre-encoded`, the 10-qualifier-prefix limit, the `add-iam-policy-binding` subcommand and deletion-protection behaviour. Removed the unconfirmed PERMISSION_DENIED outcome, the Data Boost and admin-API limitation guesses and the table-deletion claim. Also confirmed from the Bigtable access-control page that `roles/bigtable.reader` is a predefined role and that predefined roles can be granted at authorized-view level.
Method: documentation only; no commands were run.
