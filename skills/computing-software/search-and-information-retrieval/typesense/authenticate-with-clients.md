---
id: computing-software.search-and-information-retrieval.typesense.authenticate-with-clients
name: authenticate-with-clients
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [authentication, client-libraries, x-typesense-api-key, typesense]
level: intro
status: docs-checked
description: "Connect to Typesense with nodes, apiKey and timeout in each client library, pass the key by header or x-typesense-api-key parameter, and use SearchClient in browsers."
sources: ["https://typesense.org/docs/30.2/api/authentication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authenticating to Typesense

You need hostnames and API keys. Self-hosted: the IPs or DNS names of your nodes. Typesense Cloud: unique hostnames per node shown in the dashboard (like `xxx.a1.typesense.net`, port 443, protocol https).

## Client configuration

Every client takes a list of nodes (host, port, protocol; local default `localhost`, `8108`, `http`), an API key and a connection timeout. JavaScript example: `new Typesense.Client({nodes: [{host: 'localhost', port: '8108', protocol: 'http'}], apiKey: '<API_KEY>', connectionTimeoutSeconds: 2})`. Python uses `typesense.Client({'nodes': [...], 'api_key': '<API_KEY>', 'connection_timeout_seconds': 2})`. PHP, Ruby, Dart, Java and Swift clients follow the same shape.

## Browser usage

The JavaScript library works in the server and browser. In the browser use a key with search permission only, never the master key, which has write access. If you only search, `SearchClient` (imported from `typesense`) reduces bundle size.

## Raw HTTP

Send the key in the `X-TYPESENSE-API-KEY` header, or as the `x-typesense-api-key` GET parameter. Example search: `/collections/companies/documents/search?q=stark&query_by=company_name&filter_by=num_employees:>100&sort_by=num_employees:desc`.

## Checked

Method: docs-checked 2026-11-09 against the Authentication page (raw markdown of 30.2 in github.com/typesense/typesense-website, read in full). All claims confirmed.
