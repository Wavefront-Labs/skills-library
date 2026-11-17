---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.router-uri-matching
name: router-uri-matching
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, router, radixtree, uri-matching, priority, hosts, vars]
level: practitioner
status: docs-checked
description: "How the APISIX radixtree router matches routes: exact, prefix and deep wildcard URIs, parameters, priority, hosts, vars, GraphQL variables and related config.yaml limits."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/router-radixtree.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Router URI matching

URI patterns:
- Exact: `/blog/foo` matches only that path.
- Prefix: `/blog/bar*` matches `/blog/bar` and paths beneath it.
- Deep wildcard: `/blog/foo/*`.
- Parameters: with `radixtree_uri_with_parameter`, `/blog/:name` matches one segment.

Priority:
- A more specific match wins: for `/blog/foo/a/b/c`, `/blog/foo/a/*` beats `/blog/foo/*`.
- For routes sharing a URI, the route field `priority` decides; higher matches first.
- Routes with the same URI can be split by `hosts`; a non-matching host gets 404.

`vars` is a list of `[variable, operator, value]` conditions, ANDed by default. Variables include NGINX values (`http_host`, `cookie_*`, `arg_*`), form fields (`post_arg_*`), JSON body paths (`post_arg.*`) and GraphQL fields (`graphql_operation`, `graphql_name`, `graphql_root_fields`).

Settings in `config.yaml`:
- `apisix.router.http: 'radixtree_uri_with_parameter'` enables parameters.
- `apisix.match_uri_encoded_slash: true` keeps `%2F` encoded during matching; it is global and route URIs must use uppercase `%2F`.
- `graphql.max_size` caps GraphQL body reads (default 1 MiB).
- `apisix.max_post_args_readable_size` caps `post_arg.*` body reads (default 64 MB).

## Checked

2026-11-04. Confirmed against the APISIX radixtree router page: exact, prefix and deep wildcard matching and the priority table, the route priority field, hosts and the 404, vars, post_arg and GraphQL variables, radixtree_uri_with_parameter, match_uri_encoded_slash and the uppercase %2F rule, graphql.max_size 1 MiB, max_post_args_readable_size 64 MB. Nothing removed.

Method: documentation only; no commands were run.
