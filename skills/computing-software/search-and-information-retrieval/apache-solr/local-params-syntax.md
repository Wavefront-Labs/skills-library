---
id: computing-software.search-and-information-retrieval.apache-solr.local-params-syntax
name: local-params-syntax
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [local-params, query-parser-switch, localparams, dereferencing]
level: intro
status: docs-checked
description: "Use Solr local params {!type key=value} to switch query parser or set per-parameter options, with v, dereferencing, and the q.op and df overrides on a single query string."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/local-params.html
  - https://solr.apache.org/guide/solr/latest/query-guide/query-syntax-and-parsers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local-params-syntax

Local params attach metadata to one request parameter. Prefix the value with `{!` then space-separated `key=value` pairs, then `}`, followed immediately by the argument. Only one local params prefix is allowed per argument.

Example: `q={!q.op=AND df=title}solr rocks` requires both terms and searches `title` by default.

Rules:
- Values may use single or double quotes, with backslash escaping inside quotes.
- A bare value with no name gets the implicit key `type`, so `{!dismax qf=name}ipod` selects the DisMax parser.
- The main text can be supplied as `v` and can reference another request parameter by name, which keeps the user's raw text separate from the parser config.

With no type given, the Standard Query Parser is used. Local params also carry options such as `cache=false` and `cost` on filter queries.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Local Params page: `{!` prefix with whitespace-separated key=value pairs, one prefix per argument, quoting and backslash escaping, implicit `type`, the `v` key, `$qq` dereferencing, and the `q.op`/`df` example. Removed the list of other parsers, `{!tag}` and the `defType` sentence because neither fetched page states them.

Method: documentation only; no commands were run.
