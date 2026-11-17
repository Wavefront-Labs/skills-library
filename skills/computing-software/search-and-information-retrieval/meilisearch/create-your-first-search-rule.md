---
id: computing-software.search-and-information-retrieval.meilisearch.create-your-first-search-rule
name: create-your-first-search-rule
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [search-rules, pin-document, dynamic-search-rules, meilisearch]
level: practitioner
status: docs-checked
description: "Enable search rules and create a rule that pins a document to a fixed position, covering precedence, query conditions, indexUid scope and async task behaviour."
sources: ["https://www.meilisearch.com/docs/capabilities/search_rules/create_your_first_rule"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create your first search rule

Search rules are stored rules applied at search time. This guide pins one document.

## Cloud dashboard

In the project, open the Search rules tab, click Enable Search Rules, then New rule. Fields: Rule ID (cannot change later), Description, Rank (lowest number wins when several rules match), Active toggle. Choose action Pin a document with Index, Document (by primary key) and Position (starting at 1 in the dashboard). Conditions must all match; with defaults the rule applies to every search; set Query to Empty query to fire only when nothing is typed.

## Self-hosted

Search rules must first be turned on; until then the `/dynamic-search-rules` routes reject requests and stored rules do not apply. A rule example from the docs: id `invoice-help` in the URL (not the body), `precedence` 0, `conditions.query.words` equal to `invoice` (every word must appear in the query, any order), `actions.pin` with `indexUid` `support`, `id` `billing-workspace-overview`, `position` 0. Without `indexUid` the pin applies to any index holding that document id. Position counts from 0 in the API.

Creation returns a summarized task with a `taskUid`; the rule applies only once the task is `succeeded`. Fetching a rule too early answers that it does not exist. If the pinned document is missing or excluded by search filters, the pin is dropped and organic results return.

## Checked

Method: docs-checked 2026-11-09 against the Create your first rule page (raw mdx of github.com/meilisearch/documentation, read in full). Reworded the unconfirmed no-reindexing opener.
