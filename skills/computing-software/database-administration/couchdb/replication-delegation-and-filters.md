---
id: computing-software.database-administration.couchdb.replication-delegation-and-filters
name: replication-delegation-and-filters
category: computing-software
field: database-administration
product: couchdb
tags: [replication, user-ctx, selector, winning-revs-only, conflicts]
level: advanced
status: docs-checked
description: "Run replications as a delegated user with user_ctx, filter documents with a selector, and replicate only winning revisions to drop conflicts."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**user_ctx.** Replication documents persist, so who started them must be recorded. Non-admins must include `user_ctx` with their own name and a subset of their roles (enforced by the replicator database validation function; roles default to `[]`). Admins may omit it: it defaults to name `null` and no roles, so design documents are not written to local targets. To write them, include the `_admin` role. Admins may set it to run on behalf of another user; it applies only to local endpoints.

```json
"user_ctx": {"name": "joe", "roles": ["erlanger", "researcher"]}
```

**Selectors.** A `selector` in the replication document replicates only documents for which the expression is true. It uses the same syntax as `_find`, and is significantly more efficient than a JavaScript filter function; prefer it when filtering on document attributes only.

**winning_revs_only: true** (3.3.0) replicates only the revisions `GET db/doc` or default `_changes` would return. Conflicting revisions are discarded, so it can remove conflicts through replication. Replication and checkpoint IDs differ from default, so you can later backfill the rest with a regular job. It combines with filters, `continuous` and `create_target`.

## Checked

2026-11-04. Confirmed against the CouchDB replication/replicator page (Delegation, Selector Objects, Replicate Winning Revisions Only): user_ctx rules for admins and non-admins, the _admin role, local endpoints only, selector syntax and efficiency versus JavaScript filters, winning_revs_only behaviour, checkpoint ID difference and combinations. Nothing removed.

Method: documentation only; no commands were run.
