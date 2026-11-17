---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.document-and-field-level-security
name: document-and-field-level-security
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, document-and-field-level-security]
level: advanced
status: docs-checked
description: "Restrict documents with a role query and fields with field_security grant/except; understand the licence caveat."
sources:
  - https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role
  - https://docs.opensearch.org/latest/security/access-control/document-level-security/
  - https://docs.opensearch.org/latest/security/access-control/field-level-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Document-level and field-level security

**Goal:** multi-tenant data separation inside one index.
- Elasticsearch role body: `{"indices":[{"names":["orders"],"privileges":["read"],"query":{"term":{"tenant":"acme"}},"field_security":{"grant":["*"],"except":["card_*"]}}]}`. `query` is Query DSL (string or object) and a document must match it to be accessible. A role without `field_security` grants all fields, and a role without a query grants all documents. Denied fields must be a subset of granted fields.
- Multiple roles in Elasticsearch: DLS queries are combined with OR, so if any of the user's roles grants the index without DLS, no DLS applies. FLS from several roles is the union of the granted fields. Do not set field-level security on alias fields; use the concrete field name.
- Elasticsearch role definitions using DLS/FLS can be marked incompatible with the cluster licence (the role's `transient_metadata` lists them); check your licence level in Elastic's documentation.
- OpenSearch Security plugin: the REST role takes the DLS query as an escaped string in `dls` under `index_permissions`, e.g. `"dls": "{\"term\": {\"public\": true}}"`. FLS is set in Dashboards or `roles.yml` (`_fls_`), prefixing a field with `~` to exclude it; wildcards work, so exclude `title*` to cover `title.keyword`. Use either include or exclude per index, not both.
- OpenSearch combines DLS queries from several roles with OR, but a role with DLS combined with a role without DLS filters results by the DLS from the first role. FLS from several roles is evaluated with AND.
- Failure mode: combining roles gives wider or odd access than intended; test with the real combination of roles.

## Verify
- [ ] As the restricted user, `_search` returns only that tenant and masked fields.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch document and field level security page, the Elasticsearch Create or update roles API page and the OpenSearch document-level and field-level security pages (DLS page read in part, via targeted search). Confirmed role structure, `grant`/`except`, the multiple-role rules and the OpenSearch `dls` and `_fls_` forms. Removed the aggregation and alias leakage claim (only the alias-field FLS caveat is documented) and the unspecified paid-tier claim; the licence is left as a pointer.
Method: documentation only; no commands were run.
