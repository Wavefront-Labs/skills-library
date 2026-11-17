---
id: computing-software.software-engineering.quarkus.quarkus-dev-services
name: quarkus-dev-services
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, dev-services, testcontainers, dev-mode, databases, profiles]
level: practitioner
status: docs-checked
description: "Use Quarkus Dev Services to auto-start unconfigured backing services in dev and test mode, and control, disable, or override them per profile."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/dev-services.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Dev Services

Dev Services automatically provision unconfigured services in dev and test mode. Add an extension that supports Dev Services and leave its connection unconfigured; Quarkus starts the service (usually via Testcontainers) and wires the application to it.

## Requirements and timeout
Most Dev Services need a working container environment such as Docker or Podman (remote environments are supported). Without one, configure services normally. The default startup timeout is 60s; raise it with `quarkus.devservices.timeout`.

## Keep a real service in production
Use configuration profiles so only prod points at the real service and dev/test still use Dev Services:

```properties
%prod.quarkus.datasource.db-kind = postgresql
%prod.quarkus.datasource.username = prod-admin
%prod.quarkus.datasource.password = super-secret
%prod.quarkus.datasource.jdbc.url = jdbc:postgresql://localhost:5432/mydatabase
```

## Disabling
Dev Services live in the `deployment` modules and do not affect the production application. Disable all with `quarkus.devservices.enabled=false`; usually unnecessary because configuring a service's connection disables its Dev Service automatically.

## Which extension triggers which service (when the address/URL is not configured)
- AMQP: `quarkus-messaging-amqp`
- Apicurio Registry: `quarkus-apicurio-registry-avro`
- Databases: a JDBC or reactive datasource extension (all supported databases; containerised except H2, which runs in-process)
- Kafka: `quarkus-kafka-client`
- Keycloak: `quarkus-oidc`; a standalone OIDC Dev Service is a lightweight alternative, enabled by default when Docker and Podman are unavailable or with `quarkus.oidc.devservices.enabled=true`
- Kubernetes: `kubernetes-client`
- LRA: `quarkus-narayana-lra`; MongoDB: `quarkus-mongodb-client`
- RabbitMQ: `quarkus-messaging-rabbitmq`; Pulsar: `quarkus-messaging-pulsar`
- Redis: `quarkus-redis-client`; Vault: `quarkus-vault`
- Infinispan: `quarkus-infinispan-client`; Elasticsearch: Elasticsearch client or Hibernate Search ORM Elasticsearch
- Observability: `quarkus-observability-devservices` plus at least one dev resource on the classpath

## Reusing database containers
Containerised databases use Testcontainers reusable instances. Add `testcontainers.reuse.enable=true` to `.testcontainers.properties` in your user home to stop them being stopped aggressively after each run. Caveat: Quarkus will not reset database state between runs unless you configure it to.

## Beyond the platform
Quarkiverse extensions also offer Dev Services (for example Neo4j, WireMock for dev/test only, Microcks). Custom services can be defined with Quarkus Compose Dev Services using the Compose specification. Each extension's own Dev Services guide holds the detailed configuration options.

## Checked

2026-11-07. Read in full: dev-services.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
