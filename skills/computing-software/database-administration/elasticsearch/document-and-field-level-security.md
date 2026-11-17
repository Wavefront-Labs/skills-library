---
id: computing-software.database-administration.elasticsearch.document-and-field-level-security
name: document-and-field-level-security
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-security, document-level-security, field-level-security, templated-role-query, multi-tenant-search, role-query, grant-except]
level: practitioner
status: docs-checked
description: "Restrict which Elasticsearch documents and fields a role can see with document level security queries (incl. templated by user) and field level security."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Document and field level security

**Goal:** one index serves several tenants or audiences, and each user only sees their rows and allowed fields.

## Document level security (DLS)
```json
PUT _security/role/tenant_acme
{
  "indices": [ {
    "names": ["orders"],
    "privileges": ["read"],
    "query": { "term": { "tenant_id": "acme" } }
  } ]
}
```
Documents that do not match the query are not readable by users with this role. A role that sets no `query` grants all documents.

## Templated queries (per user)
```json
"query": { "template": { "source": { "term": { "tenant_id": "{{_user.metadata.tenant}}" } } } }
```
Set `metadata.tenant` on the user (custom user metadata is available as `{{_user.metadata.<key>}}`, and `{{_user.username}}` is also available); one role serves all tenants.

## Field level security (FLS)
```json
"field_security": { "grant": ["*"], "except": ["customer.ssn", "card.*"] }
```
or `"grant": ["order_id", "total", "status", "@timestamp"]`. Field expressions such as `event_*` are allowed. A role without field permissions grants all fields; the metadata fields `_id`, `_index`, `_routing` and a few others are always accessible.

## Combining roles
- A user with several roles gets the union of the permissions: a role on the same index without a `query` grants all documents, and field permissions are the union of granted fields. Check role combinations so access is not wider than intended.

## Performance and limits
- DLS/FLS depends on your subscription level; confirm on the Elastic subscriptions page.
- Elastic documents DLS/FLS as meant for read-only accounts; check the docs for your version for API features that are limited for restricted users.

## Gotchas
- DLS does not apply to write APIs: users with DLS/FLS should not perform writes, and users sharing an index need unique document ids or they can overwrite each other's documents. Give tenant roles read only, writes through the app.

## Verify
As two different tenant users, `GET orders/_count` returns different counts, and `GET orders/_doc/<other tenant id>` returns `found: false`.

## Checked

Checked 2026-10-25 against elastic/docs-content `main` (Stack 9.x docs). Confirmed: role `indices[].query` and `field_security.grant`/`except` structure, Mustache `template` queries with `_user.metadata`, union semantics across roles, roles without queries or field permissions grant everything, metadata fields always accessible, DLS does not apply to write APIs. Removed the unconfirmed bitset cache, API-limitation list and `_id` leakage claims; the licence tier is deferred to the subscriptions page. The Verify counts were not re-checked.

Method: documentation only; no commands were run.
