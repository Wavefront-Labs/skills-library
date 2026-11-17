---
id: computing-software.web-development.micronaut.micronaut-distributed-configuration
name: micronaut-distributed-configuration
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, distributed-config, consul, vault, aws-parameter-store, spring-cloud-config, bootstrap]
level: advanced
status: docs-checked
description: "Share configuration across Micronaut services via Consul, HashiCorp Vault, AWS Parameter Store or Spring Cloud Config using bootstrap settings and documented lookup paths."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cloud/cloudConfiguration/distributedConfiguration.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cloud/cloudConfiguration/distributedConfigurationConsul.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cloud/cloudConfiguration/distributedConfigurationVault.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cloud/cloudConfiguration/distributedConfigurationAwsParameterStore.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/cloud/cloudConfiguration/distributedConfigurationSpringCloud.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Distributed configuration

Goal: have several services read shared configuration from a central store.

## Which mechanism

For new work the docs recommend configuration import (`micronaut.config.import`) with custom sources via `PropertySourceImporter`, not the bootstrap context. The bootstrap approach below is described as legacy/compatibility. A `ConfigurationClient` (`getPropertySources` returns a Publisher of `PropertySource`) is the SPI; `DefaultCompositeConfigurationClient` merges all such beans. If you load config during bootstrap, you also need the discovery client infrastructure (normally `io.micronaut.discovery:micronaut-discovery-client`) and bootstrap-compatible beans.

All integrations below use `src/main/resources/bootstrap.[yml/toml/properties]` with:

```yaml
micronaut:
  application:
    name: hello-world
  config-client:
    enabled: true
```

The application name selects the per-app lookup path. Environment-specific values apply for active environments.

## Consul

Start one: `docker run -p 8500:8500 consul`. CLI: `mn create-app my-app --features config-consul`.

```yaml
consul:
  client:
    defaultZone: "${CONSUL_HOST:localhost}:${CONSUL_PORT:8500}"
```

Key/value mode reads the `/config` directory (change with `consul.client.config.path`), within these directories in the docs' order of precedence:

1. `/config/application`
2. `/config/application,prod`
3. `/config/[APPLICATION_NAME]`
4. `/config/[APPLICATION_NAME],prod`

```bash
curl -X PUT -d @- localhost:8500/v1/kv/config/application/foo.bar <<< myvalue
```

Then `@Value("${foo.bar}")` or `environment.getProperty(..)` resolves `myvalue`. To store whole YAML/JSON/properties blobs set `consul.client.config.format` (e.g. `JSON`) and PUT to `/v1/kv/config/application`. For git2consul file keys such as `/config/application.yml`, use `format: FILE`.

## HashiCorp Vault

```yaml
vault:
  client:
    uri: http://localhost:8200
    config:
      enabled: true
```

Secret paths in precedence order: `/application`, `/[APPLICATION_NAME]`, `/application/[ENV_NAME]`, `/[APPLICATION_NAME]/[ENV_NAME]`.

## AWS Parameter Store

Dependency: `io.micronaut.aws:micronaut-aws-parameter-store`. Enable with `aws.client.system-manager.parameterstore.enabled: true`. Supports `String`, `StringList` and `SecureString` (KMS decrypts automatically; if configured not to use secure strings, values come back encrypted and you decrypt manually). Environment suffix uses an underscore:

`/config/application`, `/config/[APPLICATION_NAME]`, `/config/application_prod`, `/config/[APPLICATION_NAME]_prod`.

So `/config/application_test/server.url` is read as `server.url`; `/config/myapp_test/server.url` overrides it for app `myapp`.

## Spring Cloud Config (since 1.1)

```yaml
spring:
  cloud:
    config:
      enabled: true
      uri: http://localhost:8888/
      retry-attempts: 4   # optional
      retry-delay: 2s     # optional
```

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
