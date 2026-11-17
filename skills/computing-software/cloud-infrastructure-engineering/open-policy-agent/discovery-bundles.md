---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.discovery-bundles
name: discovery-bundles
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [discovery, discovery-bundle, boot-configuration, central-config, opa-config]
level: advanced
status: docs-checked
description: "Centrally manage OPA configuration with a discovery bundle: the boot config, discovery.resource default, static JSON vs Rego, discovery.decision, and bootstrap precedence."
sources:
  - https://www.openpolicyagent.org/docs/management-discovery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change the configuration of many OPA instances from one place.

With discovery enabled OPA periodically downloads a discovery bundle, a normal bundle of JSON and Rego, evaluates it, and uses the result as the rest of its configuration (bundles, status, decision logs). Two structures:
1. static JSON files holding the configuration
2. Rego files that compute it; choose this when the policy to download depends on something dynamic such as the region OPA runs in

Boot configuration:

```yaml
services:
  acmecorp:
    url: https://example.com/control-plane-api/v1
    credentials:
      bearer:
        token: "<TOKEN>"
discovery:
  service: acmecorp
  resource: /configuration/example/discovery.tar.gz
```

OPA GETs `<services[discovery.service].url>/<discovery.resource>` and expects `200 OK` with `Content-Type: application/gzip` and a gzipped tarball.

Defaults and options:
- `discovery.resource` defaults to `bundles/<discovery.name>`, convenient when normal and discovery bundles share one endpoint.
- With a single service defined, `discovery.service` can be omitted.
- OPA queries `data` by default; set `discovery.decision` to query another path.
- `discovery.signing` takes a `keyid` and `scope` to verify the discovery bundle signature.

Precedence: manually configured plugins still work alongside discovery, and on conflict the bootstrap configuration overrides the discovered configuration.

Check: serve a discovery bundle that enables `decision_logs.console` and confirm decisions start printing without editing the boot file.

## Checked

2026-11-04. Confirmed against the OPA docs Discovery page: static JSON versus Rego discovery bundles, the boot configuration, GET with 200 OK and application/gzip, discovery.resource default bundles/<discovery.name>, optional discovery.service with one service, default query data and discovery.decision, discovery.signing keyid and scope, and bootstrap configuration overriding the discovered configuration. Nothing removed.

Method: documentation only; no commands were run.
