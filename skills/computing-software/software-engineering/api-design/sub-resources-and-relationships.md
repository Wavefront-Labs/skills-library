---
id: computing-software.software-engineering.api-design.sub-resources-and-relationships
name: sub-resources-and-relationships
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, rest, sub-resources, resource-relationships, aip-122, nested-resources, association-resources]
level: practitioner
status: docs-checked
description: "Decide between a nested sub-resource, a top-level resource with a reference field, a repeated reference list or an association sub-resource (AIP-122/124)."
sources: ["https://google.aip.dev/122", "https://google.aip.dev/124"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modelling relationships and sub-resources

## Rules from AIP-124 and AIP-122
- A resource must have at most one canonical parent, and List requests must not require two distinct "parents" to work. If a resource is many-to-one with several types, pick one as the canonical parent (it appears in the name pattern, for example `publishers/{publisher}/books/{book}`) and associate the others through reference fields.
- A reference field is a string holding the other resource's **name** (the same format as that resource's `name` field), named after the referenced message in snake case (for example `shelf`), with an `_id` suffix only if only the ID component can be used. Avoid the `_name` suffix unless ambiguous.
- Do not embed a resource message inside another resource (AIP-122): it complicates lifecycle (what happens to the embedded copy on delete?), bypasses per-resource permissions, and tightly couples schemas. Reference by name instead. Exceptions: tight internal-only lifecycle with inherited permissions, or the revisions pattern (AIP-162).
- When listing a resource that has other associations, `parent` is the only required argument; add a string `filter` so users can filter by the other associations (AIP-160).

## Decide by ownership and lifecycle
| Relationship | Model | Example |
|---|---|---|
| Child belongs to one parent | nested collection under the canonical parent | `/projects/p1/tasks/t9` |
| Independent entity that points at another | top-level resource + reference field | `/invoices/i3` with `"customer": "customers/c7"` |
| Many-to-many, simple | repeated field of resource names (AIP-144) on one resource | `repeated string authors` on a Book |
| Many-to-many with metadata, or a repeated field is too restrictive | association sub-resource with two one-to-many links | `.../books/{book}/authors/{book_author}` holding `author` plus extra fields |

AIP-124 recommends the sub-resource form for many-to-many only when the relationship needs extra metadata or the repeated-field restrictions rule that approach out; many-to-many is less common in APIs than in relational databases.

## Naming
- Resource names alternate collection identifiers (plural, camelCase) and resource IDs, separated by `/`; collection identifiers must be unique within one name (`people/xyz/people/abc` is invalid).
- A child collection may drop a redundant parent prefix (`users/u/events/e` for `UserEvent`), but do it consistently across all patterns.
- Deleting a parent that has children fails with FAILED_PRECONDITION unless the request carries `force=true` to cascade (AIP-135); singleton children do not block deletion.

## Checked
2026-11-08. Read in full: AIP-122 (resource names) and AIP-124 (resource association); AIP-135 Delete was read for the cascade rule. Removed: the JSON:API relationships source (page not read), a depth limit of one or two levels, globally unique child IDs with a shortcut `GET /comments/c`, a `:move` method, restrict-with-409 on parent delete (AIP-135 specifies FAILED_PRECONDITION), the association-resource-as-default for many-to-many (AIP-124 prefers a repeated field), and the "smells" list.
Method: documentation only; no commands were run.
