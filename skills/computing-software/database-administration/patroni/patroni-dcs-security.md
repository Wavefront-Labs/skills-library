---
id: computing-software.database-administration.patroni.patroni-dcs-security
name: patroni-dcs-security
category: computing-software
field: database-administration
product: patroni
tags: [patroni, security, dcs, tls, etcd]
level: intro
status: docs-checked
description: "Why the DCS must be protected and which authentication and TLS options Patroni offers per DCS type."
sources:
  - https://patroni.readthedocs.io/en/latest/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: lock down the store Patroni trusts.

A Patroni cluster has two interfaces to protect: the DCS and the REST API. The DCS holds no sensitive information, but it allows changing some Patroni and Postgres configuration, so it is the first thing to protect. General recommendation: enable TLS for all DCS communication.

Options by DCS type (all in the YAML settings):
- Etcd / etcd3: `username`, `password`, `cacert` (enables validation), `cert`, `key`; also `protocol` http or https.
- Consul: `token` (ACL), `scheme`, `verify`, `cacert`, `cert`, `key`. The token needs write on `service_prefix "${scope}"`, `key_prefix "${namespace}/${scope}"` and `session_prefix ""`.
- ZooKeeper: `use_ssl` (default false; all SSL parameters ignored when false), `cacert`, `cert`, `key`, `key_password`, `verify` (default true), `set_acls`, `auth_data`. SSL needs kazoo>=2.6.0.
- Raft: `password` encrypts Raft traffic and requires the cryptography Python module.

For etcd3, Patroni communicates through Etcd's gRPC-gateway (proxy), so TLS common name authentication is not possible.

Release 4.1.1 notes: Etcd security fixes in v3.6.9, v3.5.28 and v3.4.42 stopped allowing cluster topology reads and lease keepalive without authentication; Patroni now authenticates in discovery and keepalive paths and re-authenticates on failure.

Securing PostgreSQL client authentication itself is outside the document's scope.

## Checked

2026-11-03. Confirmed against the Security page and YAML Configuration Settings: per-DCS security options, ZooKeeper ssl defaults, Raft password and cryptography requirement, gRPC-gateway limitation, and the 4.1.1 release notes.

Method: documentation only; no commands were run.
