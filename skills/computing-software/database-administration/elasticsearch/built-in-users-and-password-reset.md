---
id: computing-software.database-administration.elasticsearch.built-in-users-and-password-reset
name: built-in-users-and-password-reset
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-security, elasticsearch-reset-password, built-in-users, kibana-system, elastic-user]
level: practitioner
status: verified
description: "Manage Elasticsearch built-in users (elastic, kibana_system, beats/logstash system users): reset passwords with elasticsearch-reset-password and recover a lost elastic password."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/built-in-users.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/reset-password.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-change-password.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in users and password reset

## Built-in users
| User | Purpose |
|---|---|
| `elastic` | superuser; for setup and break-glass only |
| `kibana_system` | Kibana's connection to Elasticsearch (not for humans) |
| `logstash_system`, `beats_system`, `apm_system`, `remote_monitoring_user` | monitoring data shippers |
Day-to-day: create named users or SSO roles with least privilege; use **service accounts**
(tokens) for Kibana/Fleet in 8.x rather than `kibana_system` where supported.

## Reset with the CLI (8.x)
Run on a node of the cluster (the docs: it generates and then removes a temporary user in the file realm, so it fails if the file realm is disabled):
```bash
bin/elasticsearch-reset-password -u elastic                 # auto-generates, prints it
bin/elasticsearch-reset-password -u elastic -i              # interactive: you type it
bin/elasticsearch-reset-password -u kibana_system --url https://es01:9200 -b   # -b batch, no confirmation (ran on 9.5.5: prints the new value)
```
Then update the secret wherever it is used (Kibana keystore `elasticsearch.password`, Logstash
config, monitoring agents).

## Reset via API (when you know a superuser password)
```
POST /_security/user/kibana_system/_password
{ "password": "<new strong password>" }
```

## Lost elastic password and no other superuser
`elasticsearch-reset-password` works as long as you have shell access to a node with the
correct config: it creates a temporary user in the **file realm**. If the file realm has been
disabled, temporarily add a file user:
```bash
bin/elasticsearch-users useradd breakglass -p '<pw>' -r superuser
```
(The file realm must be enabled; it is by default.) Use it to reset `elastic`, then remove it:
`bin/elasticsearch-users userdel breakglass`. File-realm users exist per node.

## Disabling unused built-ins
```
PUT /_security/user/beats_system/_disable
```
Disabling `elastic` after creating other superusers/SSO admins reduces the shared-credential risk;
keep a documented break-glass path.

## Gotchas
- 7.x used `elasticsearch-setup-passwords`; the script is still shipped in the 9.5.5 zip (`bin/elasticsearch-setup-passwords`, "Sets the passwords for reserved users") but `elasticsearch-reset-password` is the current tool.

## Verify
`curl -u elastic https://es01:9200/_security/_authenticate` returns the user with
`superuser` role using the new password; Kibana status is green after updating its credential.
