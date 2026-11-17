---
id: computing-software.database-administration.elasticsearch.service-accounts-and-tokens
name: service-accounts-and-tokens
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-security, service-account-token, elasticsearch-api-keys, kibana, fleet-server]
level: practitioner
status: verified
description: "Use Elasticsearch service accounts and service tokens for Kibana and Fleet Server instead of user passwords, and choose between service tokens and API keys for apps."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/service-accounts.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/service-tokens-command.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service accounts and tokens

**Service accounts** are fixed, built-in identities for Elastic Stack components with
predefined privileges you cannot change: `elastic/kibana`, `elastic/fleet-server`,
`elastic/fleet-server-remote` and `elastic/auto-ops` (the four returned by `GET _security/service` on 9.5.5; older versions also had `elastic/enterprise-search-server`). They authenticate with
**service tokens** (bearer tokens), not passwords.

## Create a token
API (cluster-wide):
```
POST /_security/service/elastic/kibana/credential/token/kibana-prod-1
# -> { "token": { "name": "kibana-prod-1", "value": "AAEAAWVsYXN0aWM..." } }
```
CLI (stored in `service_tokens` file on **that node only**, useful before the cluster is formed
or when the security index is unavailable):
```bash
bin/elasticsearch-service-tokens create elastic/kibana kibana-prod-1
```
List and delete:
```
GET /_security/service/elastic/kibana/credential
DELETE /_security/service/elastic/kibana/credential/token/kibana-prod-1
```

## Use it in Kibana
Configure Kibana with the token value as described in the Kibana documentation. Each Kibana instance can have its
own token name so you can revoke one without affecting others.

## Service token vs API key vs user
| Need | Use |
|---|---|
| Kibana / Fleet Server connecting to ES | service account token |
| Application or script calling ES | API key with role descriptors limited to its indices, with expiration |
| Human access | users via SSO (SAML/OIDC) or native realm with roles |
API key example:
```
POST /_security/api_key
{ "name": "orders-ingest", "expiration": "90d",
  "role_descriptors": { "ingest": { "indices": [ { "names": ["orders-*"], "privileges": ["create_doc"] } ] } } }
```

## Gotchas
- Token values are shown once; store them in a secret manager.
- CLI-created tokens exist per node; a request hitting another node fails to authenticate.
  Prefer API-created tokens in multi-node clusters.
- Service account privileges are broad for their purpose (the Kibana account can manage Kibana
  system indices); protect tokens like admin credentials.

## Verify
```
GET /_security/_authenticate      (with Authorization: Bearer <token>)
```
returns `"username": "elastic/kibana"` and `"authentication_type": "token"` (confirmed with both an API-created and a CLI-created token).
