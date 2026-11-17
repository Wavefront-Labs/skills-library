---
id: computing-software.systems-network-administration.icinga-2.api-config-objects-and-packages
name: api-config-objects-and-packages
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, rest-api, config-objects, config-packages, stages, put-post-delete, restore-attrs]
level: advanced
status: docs-checked
description: Create, modify and delete runtime objects with the Icinga 2 API using PUT, POST with attrs and restore_attrs, and DELETE with cascade, and sync them across zones.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API config objects
**Create (PUT)** `/v1/objects/<type>/<name>` with a JSON body: `templates` (optional, must already exist statically or in packages), `attrs` (required), `ignore_on_error`. Services use the full name `host!service`. Dictionary attributes accept the indexer form, `"attrs": { "vars.os": "Linux" }`. If validation fails, no object is created and the response body holds the error message.
```
curl -u root:PASSWORD -H 'Accept: application/json' -X PUT 'https://localhost:5665/v1/objects/hosts/example.localdomain' -d '{ "templates": [ "generic-host" ], "attrs": { "address": "192.168.1.1", "check_command": "hostalive" } }'
```
**Modify (POST)** with `attrs` and/or `restore_attrs`, plus a filter. `restore_attrs` makes Icinga forget the modification so DSL or Director changes apply again; setting the original value would still store it as a modified attribute. Modifications do not re-evaluate apply rules or group assignments, and resolved templates cannot be modified. Attributes such as `groups` or `zone` can be set only on PUT; `GET /v1/types` lists `no_user_modify` attributes.

**Delete (DELETE)** only objects created by the API; `cascade=1` also deletes dependants such as a host's services.

**Cluster:** set `zone` on the object; cluster nodes need `accept_config = true` on their ApiListener.

**Config packages** (`config/modify`, up to 512 MB): create a package, upload a stage of files, then list packages, stage files and stage errors, or delete a stage or package. These endpoints live under `/v1/config`.

## Checked

2026-11-04. Confirmed against the Icinga 2 API chapter: PUT/POST/DELETE object parameters, restore_attrs, no_user_modify, cascade, config packages and stages. Removed the unconfirmed claim that validation failure returns code 500.

Method: documentation only; no commands were run.
