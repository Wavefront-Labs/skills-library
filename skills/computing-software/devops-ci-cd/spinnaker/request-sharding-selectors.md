---
id: computing-software.devops-ci-cd.spinnaker.request-sharding-selectors
name: request-sharding-selectors
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [sharding, gate, orca, clouddriver, read-only-shards, selectors, dynamicendpoints]
level: sme
status: docs-checked
description: "Route Spinnaker requests to shards with selector classes (application, execution type, origin, user, account, provider): Orca shards in gate.yml, Clouddriver read/write shards."
sources:
  - https://spinnaker.io/docs/guides/runbooks/sharding-spinnaker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sharding routes traffic to different instances of a service using a **selector class** in configuration; with no selector the default endpoint is used. Netflix creates read-only Clouddriver shards, each connected to a Redis replica. Selectors exist for application, execution type (pipeline or orchestration), origin, authenticated user, deployment account and cloud provider. You must update your deployment pipelines so the infrastructure for each shard is created.

**Orca shards, in `gate.yml`:**

```yaml
services:
  orca:
    shards:
      baseUrls:
        - baseUrl: https://orca.example.com
        - baseUrl: https://orca-shard1.example.com
          priority: 10
          config:
            selectorClass: com.netflix.spinnaker.kork.web.selector.ByApplicationServiceSelector
            applicationPattern: xxxxyyyapp |demo.*xxxxyyyy
```

**Clouddriver read-only shards.** In `gate.yml`, set `services.clouddriver.baseUrl` to the read-only URL and add `config.dynamicEndpoints.deck` to send all requests from Deck to a particular shard. In `orca.yml`, list `clouddriver.readonly.baseUrls`, each with a `priority` and a selector from `com.netflix.spinnaker.orca.clouddriver.config`: `ByExecutionTypeServiceSelector` (with `executionTypes`), `ByApplicationServiceSelector` (`applicationPattern`), `ByOriginServiceSelector` (`origin: deck` plus `executionTypes`) and `ByAuthenticatedUserServiceSelector` (`users` patterns). An entry with no selector acts as the default.

**Clouddriver write-only shards**, in `orca.yml` under `clouddriver.writeonly.baseUrls`: `com.netflix.spinnaker.kork.web.selector.ByCloudProviderServiceSelector` (`cloudProviders` list), `com.netflix.spinnaker.kork.web.selector.ByAccountServiceSelector` (`accountPattern`) and `com.netflix.spinnaker.orca.clouddriver.config.ByAuthenticatedUserServiceSelector`, again with `priority` and a selector-less default entry.

The page does not state how `priority` is ordered; its examples use ascending numbers.

## Checked

2026-11-04. Selector levels, the Orca and Clouddriver YAML examples and class names were confirmed on the Sharding Spinnaker page. The write-only shards and extra selector levels were added from the same page. The page does not define priority ordering.

Method: documentation only; no commands were run.
