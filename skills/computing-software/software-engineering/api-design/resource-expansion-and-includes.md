---
id: computing-software.software-engineering.api-design.resource-expansion-and-includes
name: resource-expansion-and-includes
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, resource-expansion, expand-parameter, json-api-include, sparse-fieldsets, n-plus-one]
level: practitioner
status: docs-checked
description: "Let clients embed related resources in one call (Stripe expand, JSON:API include) with depth limits, permission checks and batched loading."
sources: ["https://docs.stripe.com/expand", "https://jsonapi.org/format/#fetching-includes", "https://learn.microsoft.com/en-us/odata/concepts/queryoptions-overview#expand"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding related resources (expand / include)

Default responses hold **references** (`"customer": "cus_123"`). Expansion swaps references for
objects on request, saving round trips.

## Syntaxes
| API style | Request | Result |
|---|---|---|
| Stripe | `?expand[]=customer&expand[]=invoice.subscription` | field replaced in place by object |
| JSON:API | `?include=author,comments.author` | related objects in top-level `included[]`, de-duplicated |
| OData | `?$expand=Customer($select=Name)` | nested |
| GraphQL | selection set | native |

## Rules
- Opt-in only; default payload stays small and cacheable.
- Allow-list expandable paths in the schema; reject unknown ones with 400.
- Limit depth (Stripe: 4 levels) and total expansions per request; expansions inside lists
  (`data.customer`) multiply cost, so meter them.
- Re-check authorization for each expanded object; a caller who can read an order may not be able
  to read the customer. Return the bare reference (or null + reason) when denied.
- Load with batching (DataLoader pattern: collect ids, one `WHERE id IN (...)`), never one query
  per row.
- Field typing: a field that is "string or object" is awkward in typed SDKs. Alternatives are a
  sibling field for the expanded object or JSON:API's `included`.
- Cache keys must include the expand parameters.
- Stripe: only properties marked "Expandable" in the API reference can be expanded, and webhook
  event objects are always sent unexpanded (fetch the object in the handler).
- JSON:API: `include` is a comma-separated list of dot-separated relationship paths; the server
  must not return unrequested resources in `included`, and a path like `comments.author` also
  returns the intermediate `comments` (full linkage).

## Verify
Query count per request stays constant as list size grows (assert in an integration test with a
query counter); unauthorized expansions don't leak data.

## Checked
2026-11-08. Confirmed in the Stripe Expand page (read by targeted search: `expand[]`, dot notation,
four-level maximum, `data.` for lists, "Expandable" label, webhooks unexpanded), the JSON:API format
page (`include` rules, `included`, no duplicates, full linkage) and the Microsoft Learn OData query
options page (`$expand` with nested options in parentheses, including `$select`). Removed unconfirmed:
the `Expandable<T>` SDK claim. The allow-list/400 rule, authorization re-check and DataLoader advice are
design guidance, not from the sources.
Method: documentation only; no commands were run.
