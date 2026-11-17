---
id: computing-software.systems-network-administration.syncthing.rest-config-endpoints
name: rest-config-endpoints
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, rest-api, rest-config, patch]
level: advanced
status: docs-checked
description: "Read and modify Syncthing configuration through granular /rest/config endpoints, with PUT, POST and PATCH semantics."
sources: ["https://docs.syncthing.net/rest/config.html", "https://docs.syncthing.net/rest/system-config-insync-get.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# /rest/config endpoints

## Behaviour
Added in version 1.12.0. These endpoints give granular access to the configuration. Config sent to them must be in the same format as returned by the corresponding GET. A successful post is applied immediately, except for changes that require a restart; query `GET /rest/config/restart-required` to check whether one is required.

## Endpoints
- `/rest/config`: GET returns everything, PUT replaces it.
- `/rest/config/folders` and `/rest/config/devices`: GET lists, PUT takes an array, POST takes one object. An existing id is replaced, a new one is added.
- `/rest/config/folders/<id>` and `/rest/config/devices/<id>`: GET returns the item, PUT replaces the entire config, PATCH replaces only the given child objects, DELETE removes it.
- `/rest/config/defaults/folder` and `/rest/config/defaults/device`: GET returns a template object with all default values (it only needs a unique ID to be applied); PUT replaces the default config (omitted values reset to the hard-coded defaults); PATCH replaces only the given child objects.
- `/rest/config/defaults/ignores` (added in 1.19.0): GET returns an object with a single `lines` array of default ignore patterns; PUT replaces it.
- `/rest/config/options`, `/rest/config/ldap`, `/rest/config/gui`: GET returns the object, PUT replaces it entirely, PATCH replaces only the given child objects.
- The `gui.password` option accepts already hashed passwords: a valid bcrypt hash is stored verbatim, a plaintext password is hashed first.

## PATCH semantics
For endpoints supporting PATCH, the existing config is taken and the given JSON object is unmarshalled on top of it, so all child objects replace the existing objects rather than extend them. The docs' example: `RawListenAddresses` in options is an array of strings, and sending `{RawListenAddresses: ["tcp://10.0.0.2"]}` replaces all existing listen addresses.

## Deprecated
`GET /rest/system/config/insync` (deprecated since 1.12.0) returns `configInSync`, whether the running configuration is the same as that on disk; use `/rest/config/restart-required` instead.

## Checked
2026-11-04. Read the Config Endpoints page and the deprecated insync page: version notes, immediate application, each endpoint's verbs, PATCH replacement semantics and the example, bcrypt handling and the deprecation. Removed the curl PATCH example (its field name is not shown on the page), the "Safe workflow" advice and the `syncthing cli config` claim.
Method: documentation only; no commands were run.
