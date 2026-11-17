---
id: computing-software.software-engineering.api-design.soft-delete-and-singleton-resources
name: soft-delete-and-singleton-resources
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, soft-delete, singleton-resources, aip-164, aip-156, undelete, purge]
level: practitioner
status: docs-checked
description: "Implement soft delete with undelete, delete_time, purge_time and show_deleted, and model singleton sub-resources with get/update but no create or delete."
sources: ["https://google.aip.dev/164", "https://google.aip.dev/156", "https://google.aip.dev/135"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soft delete and singleton resources

## Soft delete (AIP-164)
Soft delete is optional ("APIs may support") and exists for recovery from mistakes.
- Delete only marks the resource as deleted without removing it, and then should return the updated resource instead of `google.protobuf.Empty` (AIP-135 says the same).
- The resource should have `delete_time` and `purge_time` fields (per AIP-148), and a `DELETED` state value if it has a `state` field. `purge_time` was renamed from `expire_time` in 2023.
- Provide an Undelete method: HTTP `POST`, body `"*"`, URI like `/v1/{name=publishers/*/books/*}:undelete`, response is the resource itself (a long-running operation resolving to the resource if slow). The request has only a required `name` field.
- `List` does not return soft-deleted resources unless `bool show_deleted` is true. `Get` of a soft-deleted resource should return it rather than NOT_FOUND.
- Purge strategy is your choice (automatic after a reasonable time such as 30 days, user-set expiry, or indefinite retention), but document when soft-deleted resources are completely removed.
- Optional Expunge custom method (`:expunge`, POST, body `"*"`, returns Empty or an Operation) permanently deletes immediately; it works on resources in CREATING, READY or SOFT_DELETED states, and requires a separate explicit expunge permission distinct from delete.
- Errors: no permission gives PERMISSION_DENIED (403), checked before existence; missing or already expunged gives NOT_FOUND (404); soft-deleting an already-deleted resource succeeds if `allow_missing` is true and otherwise should be NOT_FOUND; Undelete on a resource that is not deleted gives ALREADY_EXISTS (409); Expunge on a resource not in a ready or soft-deleted state gives FAILED_PRECONDITION (400).
- Trade-off: a soft-deleted ID cannot be reused unless Undelete is called, which is awkward for declarative clients.

## Singleton resources (AIP-156)
A resource with exactly one instance per parent, existing because its parent does: `users/1234/config`.
- No user-provided or system-generated ID: the name is the parent's name plus one static segment, and the segment is singular.
- Must not define Create or Delete standard methods; it is created and deleted with its parent. Should define Get and Update (but not Update if every field is output only), and may define custom methods.
- The resource definition must give both `singular` and `plural`.
- Update is a PATCH on the fixed name, for example `/v1/{config.name=users/*/config}`.
- List is optional and must follow AIP-159: it uses the plural (`/v1/{parent=users/*}/configs`), `users/-` lists all configs, and a real user ID returns a collection of one (use Get instead).
- When deleting a parent, singleton children do not block deletion, though other child types do (FAILED_PRECONDITION unless `force`, per AIP-135).

## Verify
Test: delete, then list hides it, `show_deleted` shows it, undelete restores it; after purge, Get returns 404.

## Checked
2026-11-08. Read in full: AIP-164, AIP-156 and AIP-135 (google.aip.dev). Corrected: `expire_time` is now `purge_time`; the draft's undelete errors (400/409) and delete behaviour for unique names were replaced with the AIP's error table. Removed unsupported advice: database `deleted_at` columns and partial indexes, privacy-law note, 409 on re-creating a deleted name, PUT for singletons, and the `:reset` custom method suggestion (AIP-156 only says custom methods may be defined).
Method: documentation only; no commands were run.
