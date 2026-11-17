---
id: computing-software.messaging-and-integration.apache-camel.property-placeholders
name: property-placeholders
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, configuration, properties, placeholders, endpoints]
level: practitioner
status: docs-checked
description: "Camel property placeholder syntax: defaults, optional {{?key}}, boolean negation {{!key}}, nested placeholders, escaping, where they work and Kubernetes locations."
sources:
  - https://camel.apache.org/manual/using-propertyplaceholder.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property placeholders

Syntax:
- `{{key}}` basic, e.g. `{{file.uri}}`.
- `{{file.url:/some/path}}` default after a colon.
- `{{?myBufferSize}}` optional: if missing, the endpoint option is left unset so the component default applies.
- `{{!integration.ftpEnabled}}` negates a boolean, handy for `autoStartup`.

Usable in endpoint URIs (even `mock:{{where}}`), endpoint options (`file:outbox?bufferSize={{buf}}`), route attributes such as `autoStartup`, and `ProducerTemplate`/`ConsumerTemplate` calls.

Nested: a value may reference another key (`cool.concat=mock:{{cool.foo}}`). Disable per key with `{{myQuery?nested=false}}` (useful for JSON ending in `}}`), or globally with `setNestedPlaceholder(false)` on the Properties component.

Escape with `\{{ name \}}` to output a literal `{{ name }}`.

Sources: the Properties component loads configured locations (e.g. `application.properties`). On Kubernetes set `camel.main.cloud-properties-location` to comma-separated mounted Secret or ConfigMap paths. Custom sources implement `PropertySource` (or `LoadablePropertiesSource`), registered in `META-INF/services/org/apache/camel/property-source-factory`.

Spring XML non-string attributes use the `prop:` namespace (`http://camel.apache.org/schema/placeholder`), e.g. `prop:stopOnException="stop"`, whose value is the key, not `{{...}}`.

Java: `getPropertiesComponent().resolveProperty("foo")` returns `Optional<String>`; `camelContext.resolvePropertyPlaceholders(text)` resolves a string.

Verify: a route using `{{missing:fallback}}` starts with the fallback value.

## Checked

Method: docs-checked 2026-11-09 against https://camel.apache.org/manual/using-propertyplaceholder.html
