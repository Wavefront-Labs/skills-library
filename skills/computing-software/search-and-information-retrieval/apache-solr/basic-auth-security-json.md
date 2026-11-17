---
id: computing-software.search-and-information-retrieval.apache-solr.basic-auth-security-json
name: basic-auth-security-json
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [basic-auth, basic-authentication, security-json, blockunknown, auth-enable, basicauthplugin]
level: practitioner
status: docs-checked
description: "Turn on Solr Basic authentication with bin/solr auth enable or security.json: BasicAuthPlugin, blockUnknown, credentials, realm, forwardCredentials, ZooKeeper upload."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/basic-authentication-plugin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# basic-auth-security-json

In cloud mode, `bin/solr auth enable` applies a best-practice template with preconfigured roles and permissions. Alternatively write `security.json` with an `authentication` block naming the plugin class (`solr.BasicAuthPlugin`).

Keys:
- `blockUnknown`: defaults to true when omitted. If false, any request not covered by a permission is open to anonymous users. Keep it true (or omitted) to enforce authentication for all requests.
- `credentials`: map of user to `base64(sha256(sha256(salt+password))) base64(salt)`. If you edit the file by hand you must produce this hash yourself.
- `realm`: login prompt text; defaults to `solr`.
- `forwardCredentials`: false lets Solr's PKI authentication handle node-to-node requests instead of forwarding the Basic header.

In SolrCloud, `security.json` must be uploaded to ZooKeeper. Pair the authentication block with an `authorization` block, which can include a role binding for the `all` permission in the last position.

Manage users afterward through the authentication API commands (such as `set-user` and `delete-user`).

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Basic Authentication Plugin page: `bin/solr auth enable` in cloud mode, the `authentication` block, `blockUnknown` default and the anonymous-access warning with the `all` permission last, the credentials hash format and manual encoding, `realm` default `solr`, `forwardCredentials`, ZooKeeper upload in SolrCloud, and the `set-user` / `delete-user` API commands. Nothing removed.

Method: documentation only; no commands were run.
