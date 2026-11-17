---
id: computing-software.messaging-and-integration.temporal.service-configuration-tls-auth
name: service-configuration-tls-auth
category: computing-software
field: messaging-and-integration
product: temporal
tags: [static-configuration, development-yaml, tls, mutual-tls, authorizer, claim-mapper, jwt-key-provider, membership, prometheus]
level: advanced
status: docs-checked
description: "Temporal self-hosted static config (development.yaml): global membership, metrics, pprof, TLS internode and frontend, mutual TLS, authorizer, claimMapper and JWT key provider."
sources:
  - https://docs.temporal.io/references/service-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Static configuration lives in `development.yaml`; changes need a process restart (use dynamic configuration for live tuning). Top-level sections: `global`, `persistence`, `log`, `clusterMetadata`, `services`, `publicClient`, `archival`, `namespaceDefaults`, `dcRedirectionPolicy`, `dynamicConfigClient`.

`global.membership`: `maxJoinDuration` (default `10s`) bounds gossip joining; `broadcastAddress` must be an IPv4 address other hosts can reach (`127.0.0.1` for a single host).

`global.metrics`: `prefix`, `tags`, `excludeTags` (map of tag name to values; drops unbounded tags such as `task_queue`). `prometheus` takes `framework` (`tally` default, or `opentelemetry`), `listenAddress` and `handlerPath` (default `/metrics`). statsd is not natively supported. `global.pprof.port` starts pprof at process start.

`global.tls` has `internode` (between service roles) and `frontend` (SDK clients). Each has `server` (`certFile`, `keyFile`, `requireClientAuth`, `clientCaFiles`; the latter ignored when client auth is off) and `client` (`serverName`, `rootCaFiles`). Roles dial each other by IP, so set `serverName` unless certificates carry IP SANs. With client auth on, roles reuse the `internode.server` certificate as client certificate: set it on every role, mint it with no EKUs or both ServerAuth and ClientAuth, and add its CA to `internode.server.clientCaFiles`, `internode.client.rootCaFiles` and `frontend.server.clientCaFiles` when hosts do not trust it.

`global.authorization`: `authorizer` and `claimMapper` default to empty (everything allowed); `default` enables the built-in role-based authorizer and JWT mapper. `audience` (empty skips check), `authHeaderName` (default `authorization`). `jwtKeyProvider.keySourceURIs` lists JWKS URLs; `refreshInterval` defaults to `0`, so keys load once and never rotate. `remoteClusterAuth.require: true` fails outbound replication RPCs with `Unauthenticated` on empty tokens and blocks startup without a `TokenProvider`.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: references/service-configuration (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
