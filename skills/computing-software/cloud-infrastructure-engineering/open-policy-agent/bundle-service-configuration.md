---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.bundle-service-configuration
name: bundle-service-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [bundles, bundle-service, persist, services-config, resource-path]
level: practitioner
status: docs-checked
description: "Configure OPA to download bundles from an HTTP service: resource path defaulting to bundles/<name>, 200 gzip contract, persist for offline start, and signing keyid."
sources:
  - https://www.openpolicyagent.org/docs/management-bundles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep OPA's policy and data current from a remote HTTP server.

OPA calls `GET /<service path>/<resource>`. The server answers `200 OK`, `Content-Type: application/gzip`, with a gzipped tarball.

URL composition: `services[0].url` plus `bundles[_].resource`, for example `https://example.com/service/v1` plus `somedir/bundle.tar.gz`.

If `bundles[_].resource` is unset it defaults to `bundles/<name>`, where `name` is the key under `bundles`. Names may contain any valid YAML characters including `/`, so a bundle named `authz/bundle.tar.gz` fetches `bundles/authz/bundle.tar.gz`.

```yaml
services:
- name: acmecorp
  url: https://example.com/service/v1
  credentials:
    bearer:
      token: "<TOKEN>"
bundles:
  authz:
    service: acmecorp
    resource: somedir/bundle.tar.gz
    persist: true
    signing:
      keyid: my_global_key
      scope: read
```

Persistence: set `persist: true` and OPA writes each activated bundle to disk and reads it at startup, so it can start with the last activated bundle when the bundle server is unreachable. Loading is best effort; errors appear in the bundle's status update. When connectivity returns, the latest bundle is downloaded, activated and persisted. The default location is under the working directory, `./.opa/bundles/<bundle-name>/bundle.tar.gz`.

`signing` carries the `keyid` and `scope` used to verify the bundle signature.

Check: stop the bundle server, restart OPA, and confirm it still serves decisions from the persisted bundle while the status report shows the download error.

## Checked

2026-11-04. Confirmed against the Bundles page section Bundle Service API: GET request shape, 200 OK with application/gzip, URL composition, default resource bundles/<name>, names with slashes, persist behaviour and default ./.opa/bundles/<bundle-name>/bundle.tar.gz, signing keyid and scope. Nothing removed.

Method: documentation only; no commands were run.
