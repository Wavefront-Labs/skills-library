---
id: computing-software.database-administration.couchdb.config-via-http-api
name: config-via-http-api
category: computing-software
field: database-administration
product: couchdb
tags: [configuration, http-api, config-whitelist, local-node, bind-address]
level: practitioner
status: docs-checked
description: "Change CouchDB settings at runtime via /_node/{node}/_config without a restart, use _local for the current node, and guard with config_whitelist."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/intro.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set a parameter on the fly, no restart needed:

```
curl -X PUT http://adm:pass@localhost:5984/_node/<name@host>/_config/uuids/algorithm -d '"random"'
```

The response is the old value, such as `"sequential"`. Use the literal `_local` instead of a node name for the local node:

```
curl -X PUT http://adm:pass@localhost:5984/_node/_local/_config/uuids/algorithm -d '"random"'
```

**Risk.** You can make CouchDB unreachable, for example by setting `chttpd/bind_address` to a typo or an unavailable IP. The only fix is to log in to the server, correct the config file and restart.

**Guard.** Set `chttpd/config_whitelist` to the parameters permitted for HTTP API updates. Changes to non-whitelisted parameters must then go through the config file, and in most cases need a restart.

## Checked

2026-11-04. Confirmed against the CouchDB config/intro page: the PUT on _node/.../_config, old value returned, _local, the bind_address risk and config_whitelist behaviour. Removed an unconfirmed claim about which file runtime changes are written to.

Method: documentation only; no commands were run.
