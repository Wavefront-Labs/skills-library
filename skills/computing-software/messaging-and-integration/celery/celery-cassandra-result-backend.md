---
id: computing-software.messaging-and-integration.celery.celery-cassandra-result-backend
name: celery-cassandra-result-backend
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-other-backends, celery, cassandra, astra-db, result-backend, consistency, auth-provider]
level: practitioner
status: docs-checked
description: "Configure the Celery Cassandra or Astra DB result backend: servers vs secure bundle, consistency levels, TTL, auth and driver options."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cassandra / Astra DB result backend

Goal: store results in Cassandra or Astra DB. Install `pip install celery[cassandra]` (needs `cassandra-driver`). Exactly one of `cassandra_servers` and `cassandra_secure_bundle_path` must be provided, never both.

## Settings
- `cassandra_servers` (default `[]`): e.g. `['localhost']`.
- `cassandra_secure_bundle_path` (None): absolute path to the secure-connect-bundle zip for Astra DB.
- `cassandra_port` (9042), `cassandra_keyspace` (None), `cassandra_table` (None).
- `cassandra_read_consistency` / `cassandra_write_consistency` (None): `ONE`, `TWO`, `THREE`, `QUORUM`, `ALL`, `LOCAL_QUORUM`, `EACH_QUORUM`, `LOCAL_ONE`.
- `cassandra_entry_ttl` (None = never expire): seconds.
- `cassandra_auth_provider` (None): `PlainTextAuthProvider` or `SaslAuthProvider`; `cassandra_auth_kwargs` (`{}`) are its named arguments.
- `cassandra_options` (`{}`): arguments for the `cassandra.cluster` class.

## Example (Cassandra)
```python
result_backend = 'cassandra://'
cassandra_servers = ['localhost']
cassandra_keyspace = 'celery'
cassandra_table = 'tasks'
cassandra_read_consistency = 'QUORUM'
cassandra_write_consistency = 'QUORUM'
cassandra_entry_ttl = 86400
```

## Example (Astra DB)
Use `PlainTextAuthProvider` with the token Client ID as username and Client Secret as password:
```python
result_backend = 'cassandra://'
cassandra_keyspace = 'celery'
cassandra_table = 'tasks'
cassandra_auth_provider = 'PlainTextAuthProvider'
cassandra_auth_kwargs = {
  'username': '<<CLIENT_ID_FROM_ASTRA_DB_TOKEN>>',
  'password': '<<CLIENT_SECRET_FROM_ASTRA_DB_TOKEN>>'
}
cassandra_secure_bundle_path = '/path/to/secure-connect-bundle.zip'
```

## Explicit load balancing
The driver negotiates protocol version and automatically supplies `DCAwareRoundRobinPolicy`; future driver versions will require the policy. Provide both explicitly:
```python
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.cluster import ExecutionProfile, EXEC_PROFILE_DEFAULT
myEProfile = ExecutionProfile(
  load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'))
cassandra_options = {
  'protocol_version': 5,   # for Cassandra 4; the docs use 4 for Astra DB
  'execution_profiles': {EXEC_PROFILE_DEFAULT: myEProfile},
}
```
For Astra DB the region name is the DC name (e.g. `europe-west1`).

## 5.7 consistency note
Workers also use the read consistency when storing a result: each write attempt first reads the newest row and skips the write if it is `SUCCESS` (one extra read per write). A read level stricter than the write level can make writes fail while nodes are down; a weaker one (such as `ONE`) can miss a `SUCCESS` stored on another replica. Overlapping runs of the same task can still both write.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
