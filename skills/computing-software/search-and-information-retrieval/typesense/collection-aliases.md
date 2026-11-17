---
id: computing-software.search-and-information-retrieval.typesense.collection-aliases
name: collection-aliases
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [collection-alias, zero-downtime-reindex, aliases-api, typesense]
level: practitioner
status: docs-checked
description: "Use Typesense aliases as virtual collection names to reindex into a new collection and switch with PUT /aliases/:alias, plus retrieve, list and delete."
sources: ["https://typesense.org/docs/30.2/api/collection-alias.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collection aliases

An alias is a virtual collection name pointing at a real collection, like a Linux symbolic link. Anywhere an API call takes a collection name you can pass the alias; Typesense resolves it internally for searches, writes and so on.

## Reindexing pattern

Alias `companies` points to `companies_june10`, and the application always searches `"collection": "companies"`. On the next day create `companies_june11`, index into it in the background, then repoint the alias to it. The application switches immediately with no code change.

## API

- Create or update: `PUT /aliases/:alias` with `{"collection_name": "companies_june11"}`. Response: `{"name": "companies", "collection_name": "companies_june11"}`. `collection_name` is required. Client form: `client.aliases().upsert('companies', {collection_name: 'companies_june11'})`.
- Retrieve one: `GET /aliases/:alias`.
- List all: `GET /aliases`, returning an `aliases` array of name/collection_name pairs.
- Delete: `DELETE /aliases/:alias`, which returns the deleted mapping.

Every call needs the `X-TYPESENSE-API-KEY` header.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Collection Alias page (https://typesense.org/docs/30.2/api/collection-alias.html). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
