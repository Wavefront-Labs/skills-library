---
id: computing-software.messaging-and-integration.apache-camel.route-templates
name: route-templates
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, route-template, templated-route, parameters, reuse]
level: practitioner
status: docs-checked
description: "Camel route templates: routeTemplate and templateParameter with defaults, templatedRoute creation, TemplatedRouteBuilder, prefixId and placeholder rules."
sources:
  - https://camel.apache.org/manual/route-template.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route templates

A route template is a parameterised route; one template can create many routes.

```java
routeTemplate("myTemplate")
    .templateParameter("name")
    .templateParameter("myPeriod", "3s")
    .from("timer:{{name}}?period={{myPeriod}}")
        .log("tick");
```

- Template ids must be unique. The second argument to `templateParameter` is a default.
- Inside the route `{{name}}` refers to a parameter. A template parameter overrides a same-named property, so a value must be supplied.
- `{{?name}}` is optional (option left unset when null); `{{!name}}` negates a boolean.
- Optional parameters (`templateOptionalParameter`, XML `required="false"`) let `{{?uri}}` on `to`, `toD`, `wireTap`, `enrich`, `pollEnrich` or `poll` be skipped.

Creating routes:
- Java DSL: `templatedRoute("id").parameter(...)`.
- API: `TemplatedRouteBuilder.builder(context, "id").parameter(...).add()`; `add()` returns the route id, or `null` if the context has not started.
- XML/YAML: `templatedRoute` with `routeTemplateRef`.
- Without `routeId(...)`, ids are auto-assigned (`route1`...).

Hardcoded node ids are reused in every created route. Camel gives each route its own prefix, but two routes created with the same prefix raise a duplicate-id error, so set a distinct `prefixId(...)` per route.

Template beans are private per created route. In Java, do not use the Simple fluent builder with parameters; use `simple("'{{color}}' == 'red'")`. camel-main sets parameters with keys like `camel.route-template[0].template-id`.

Verify: creating two routes from one template with different `name` values yields two started routes with distinct ids.

## Checked

Method: docs-checked 2026-11-09 against https://camel.apache.org/manual/route-template.html
