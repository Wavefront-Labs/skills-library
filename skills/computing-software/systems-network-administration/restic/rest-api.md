---
id: computing-software.systems-network-administration.restic.rest-api
name: rest-api
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, rest-api, http, rest-server, backend-protocol, api-v2]
level: sme
status: docs-checked
description: "The restic REST backend HTTP API: endpoints for repository, config and blob types, API version negotiation by Accept header, ranges and status codes."
sources:
  - https://raw.githubusercontent.com/restic/restic/master/doc/REST_backend.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REST backend API

The base path `{path}` selects a repository (default `/`) and must end with a slash. Valid `{type}` values: `data`, `keys`, `locks`, `snapshots`, `index`, `config`.

## Version negotiation

Send `Accept: application/vnd.x.restic.rest.v2` for API v2; an empty value or `application/vnd.x.restic.rest.v1` selects v1. JSON responses carry the highest supported version in `Content-Type`; any value other than v2 means v1. Binary payloads use `binary/octet-stream`.

## Repository

- `POST {path}?create=true` creates the structure; 200 if created or already existing.
- `DELETE {path}` deletes the repository: 200, 501 if unsupported, 403 if denied.

## Config

- `HEAD {path}/config`: 200 if present
- `GET {path}/config`: returns the content
- `POST {path}/config`: stores the body

## Listing

`GET {path}/{type}/` returns, in v1, a JSON array of names; in v2, an array of objects with `name` and `size` in bytes.

## Blobs `{path}/{type}/{name}`

- `HEAD`: 200 if present (with `Content-Length`), else 404
- `GET`: content, 404 if missing; a `Range` header returns 206 with the requested part
- `POST`: stores the request body
- `DELETE`: 200 on success

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/restic/restic/master/doc/REST_backend.rst.

Method: documentation only; no commands were run.
