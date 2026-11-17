---
id: computing-software.messaging-and-integration.temporal.service-configuration-persistence-cluster
name: service-configuration-persistence-cluster
category: computing-software
field: messaging-and-integration
product: temporal
tags: [persistence-config, num-history-shards, datastores, cluster-metadata, dc-redirection-policy, public-client, archival-config, membership-port]
level: advanced
status: docs-checked
description: "Temporal static config persistence, clusterMetadata, services rpc, publicClient, archival and dcRedirectionPolicy: required keys, defaults and the immutable numHistoryShards."
sources:
  - https://docs.temporal.io/references/service-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`persistence` needs `numHistoryShards` (set at first start, immutable afterward, later changes ignored; size for peak load), `defaultStore` (workflow state), `visibilityStore`, optional `secondaryVisibilityStore` (Dual Visibility) and `datastores`, named definitions each exactly one of `cassandra`, `sql`, `elasticsearch`, `customDatastore`.
- cassandra: `hosts` and `keyspace` required; `port` default 9042; `user`, `password`, `datacenter`, `maxConns`, `tls`.
- sql: `pluginName` (`mysql` or `postgres`), `databaseName`, `connectAddr`, `connectProtocol` (`tcp` or `unix`) required; `maxConns`, `maxIdleConns`, `maxConnLifetime`, `connectAttributes`.
- datastore `tls`/`mtls`: `enabled`, `serverName`, `certFile`, `keyFile`, `caFile`, `enableHostVerification` (inverse of Go InsecureSkipVerify).

`log`: `stdout`, `level` (debug, info default, warn, error, fatal), `outputFile`.

`clusterMetadata`: `currentClusterName` required and immutable; `enableGlobalNamespace` default false; `failoverVersionIncrement`; `masterClusterName` (only it can register or update Namespaces; any cluster can fail over); `clusterInformation` entries with `enabled`, `initialFailoverVersion`, `rpcAddress` (prefix `dns:///` to round-robin DNS IPs).

`services`: roles `frontend`, `internal-frontend`, `matching`, `worker`, `history`. Each needs `rpc` with `grpcPort`, `membershipPort` (distinct per role, and per Temporal Service sharing a network), and `bindOnIP` or `bindOnLocalHost` (not both).

`publicClient`: omit it to reach `internal-frontend` or `frontend` via membership; set `hostPort` for a fixed endpoint. Configuring both an `internal-frontend` role and a publicClient prevents startup.

`archival.history` and `archival.visibility`: `state`, `enableRead`, `provider` (`filestore`, `gstorage`, `s3store`); `namespaceDefaults.archival` sets `state` and `URI` for new Namespaces.

`dcRedirectionPolicy.policy`: `noop` (default), `selected-apis-forwarding` (start, signal, signal-with-start, cancel, terminate, query) or `all-apis-forwarding`.

`dynamicConfigClient`: `filepath` and `pollInterval` (minimum 5s).

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: references/service-configuration (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
