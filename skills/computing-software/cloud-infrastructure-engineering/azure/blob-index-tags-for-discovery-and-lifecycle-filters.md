---
id: computing-software.cloud-infrastructure-engineering.azure.blob-index-tags-for-discovery-and-lifecycle-filters
name: blob-index-tags-for-discovery-and-lifecycle-filters
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, blob-storage, blob-index-tag-queries, find-blobs-by-tags, blob-index-tags, lifecycle-filters]
level: practitioner
status: docs-checked
description: "Use blob index tags: set and read tags, find blobs across containers with tag filters, drive lifecycle rules and ABAC from tags, plus limits, cost and HNS restrictions."
sources: ["https://learn.microsoft.com/azure/storage/blobs/storage-manage-find-blobs", "https://learn.microsoft.com/azure/storage/blobs/storage-blob-index-how-to", "https://learn.microsoft.com/cli/azure/storage/blob/tag"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blob index tags

**Goal:** a queryable key/value index over blobs (by project, status, retention class) without an external database.

## Set and read
```bash
az storage blob tag set --account-name st --container-name docs --name invoices/2026/10/inv-881.pdf \
  --tags Project=Contoso Status=Final --auth-mode login
az storage blob tag list --account-name st --container-name docs --name invoices/2026/10/inv-881.pdf --auth-mode login
```
Or set at upload: `az storage blob upload ... --tags Project=Contoso`.
Limits: up to **10 tags per blob**; key 1-128 chars, value 0-256 chars; case-sensitive; only string values; characters limited to
letters, digits and space, plus, minus, period, colon, equals, underscore and forward slash. With versioning enabled, tags belong to a specific version: a new version does not inherit the tags set on the previous current version.

## Find blobs (account-wide or per container)
```bash
az storage blob filter --account-name st --tag-filter "\"Project\"='Contoso' AND \"Status\"='Final'" --auth-mode login
az storage blob filter --account-name st --container-name docs --tag-filter "\"Year\">='2025'" --auth-mode login
```
Operators: `=`, `>`, `>=`, `<`, `<=` (lexicographic string comparison, so zero-pad numbers/dates) and `AND`. Tag queries are optimised for
equality on a single tag; range queries on a single tag are also efficient, and AND queries over several tags are slower. Index tags are not passed to the index for previous versions, so you cannot query for old versions by tag.

## Use with lifecycle and access control
- Lifecycle filter: `"filters": {"blobTypes":["blockBlob"], "blobIndexMatch":[{"name":"Retention","op":"==","value":"Short"}]}`.
- ABAC role-assignment conditions can reference blob index tags to restrict reads and writes.

## Permissions
Setting tags is allowed for Storage Blob Data Owner, for anyone with a SAS that has the `t` permission, and for RBAC principals with
`Microsoft.Storage/storageAccounts/blobServices/containers/blobs/tags/write`. Reading and filtering need their own tag permissions (`.../tags/read`, `.../filter/action`); check the built-in role definitions.

## Gotchas
- **Indexing is not available on hierarchical namespace (ADLS Gen2) accounts**; tags without indexing are in preview there and are not integrated with lifecycle management.
- You are charged for the monthly average number of index tags, plus list transactions for tag queries; not free metadata.
- Tags are separate from blob metadata: metadata is not indexed or searchable; setting tags doesn't change ETag or last-modified time.

## Verify
- [ ] Filter query returns the expected set; lifecycle rule using `blobIndexMatch` acts on tagged blobs only.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/blobs/storage-manage-find-blobs, storage-blob-index-how-to): 10-tag limit, key/value length and character rules, case sensitivity, string-only values, query operators and lexicographic comparison, versioning behaviour, HNS limitation (indexing unavailable, preview without indexing), tag permissions, billing basis, CLI commands `az storage blob tag set|list`, `az storage blob upload --tags`. Removed the unconfirmed eventual-consistency and copy-tag statements and the Contributor role claim.

Method: documentation only; no commands were run.
