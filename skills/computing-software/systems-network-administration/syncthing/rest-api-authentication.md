---
id: computing-software.systems-network-administration.syncthing.rest-api-authentication
name: rest-api-authentication
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, rest-api, api-key, pagination]
level: practitioner
status: docs-checked
description: "Authenticate to the Syncthing REST API with X-API-Key or a Bearer token and use page and perpage pagination."
sources: ["https://docs.syncthing.net/dev/rest.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REST API authentication and basics

## API key
Syncthing exposes a REST interface over HTTP on the GUI port; in most cases input and output are JSON. An API key must be set and used. It can be generated in the GUI or set in the `configuration/gui/apikey` element. Send it either way:

```sh
curl -H "X-API-Key: <key>" http://127.0.0.1:8384/rest/system/status
curl -H "Authorization: Bearer <key>" http://127.0.0.1:8384/rest/system/status
```
Add `-k` when using HTTPS with a Syncthing-generated or self-signed certificate. The `--gui-apikey` command-line option overrides the API key.

## Exception
`/rest/noauth` endpoints need no API key, so third-party devices and services can make simple calls that do not expose sensitive information without exposing your key.

## Pagination
Some GET endpoints take optional `page` and `perpage` arguments. No more than `perpage` entries (defaults to 65536 if not given) are returned in an array; passing `page` advances through the results, and the parameters actually used are always returned as attributes in the response object.

## Related endpoints
The index page lists, among others, `GET /rest/system/status`, `GET /rest/system/browse`, `POST /rest/system/pause`, `POST /rest/system/resume`, `POST /rest/system/restart`, `POST /rest/system/shutdown`, `/rest/config/...`, and the cluster, folder and db endpoints. See each endpoint's page for parameters.

The docs say the interface is subject to change.

## Checked
2026-11-04. Read the REST API page and the Command Line Operation page (`--gui-apikey`): both header forms, the `-k` note, `/rest/noauth` exception, pagination wording and defaults, and the endpoint index. Removed the `/rest/noauth/health` example, the endpoint parameters and `restart-required` path that the index page does not give, and the unsupported "full control" caution.
Method: documentation only; no commands were run.
