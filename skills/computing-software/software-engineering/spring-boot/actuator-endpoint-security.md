---
id: computing-software.software-engineering.spring-boot.actuator-endpoint-security
name: actuator-endpoint-security
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, actuator, security, endpointrequest, securityfilterchain, csrf, sanitization, cors]
level: practitioner
status: docs-checked
description: "Secure Actuator endpoints with Spring Security and EndpointRequest, CSRF behaviour, sanitizing env/configprops values, response caching, CORS and the JSON mapper."
sources:
  - https://docs.spring.io/spring-boot/reference/actuator/endpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Security defaults: if Spring Security is on the classpath and no other `SecurityFilterChain` bean exists, all actuators other than `/health` are secured by auto-configuration. Defining any `SecurityFilterChain` bean makes it back off completely, giving you full control of actuator rules and the rest of the application (add a chain for the rest too). Use the `EndpointRequest` matchers (for example `EndpointRequest.toAnyEndpoint()`) with Spring Security; `EndpointRequest.to("endpoint")` matches the endpoint root and all subpaths (`/actuator/endpoint/**`). To allow unauthenticated access behind a firewall, set `management.endpoints.web.exposure.include: "*"` and add a chain permitting actuator requests.

CSRF: Spring Security defaults leave CSRF on, so endpoints needing `POST` (shutdown, loggers), `PUT` or `DELETE` return 403 with the default configuration. Disable CSRF completely only for a service used by non-browser clients.

Sanitization: values from `/env`, `/configprops` and `/quartz` are fully sanitized (`******`) by default. Set `show-values` per endpoint to `never`, `always` or `when-authorized`; unsanitized values show only if no custom `SanitizingFunction` bean applies. Authorized for HTTP means authenticated with the endpoint's configured `roles` (any authenticated user if none); JMX users are always authorized.
```yaml
management:
  endpoint:
    env:
      show-values: when-authorized
      roles: "admin"
```

Caching: read operations without parameters are cached; set `management.endpoint.<name>.cache.time-to-live`, for example `beans` to `"10s"`.

CORS: disabled until `management.endpoints.web.cors.allowed-origins` is set, for example with `allowed-methods: "GET,POST"` (see `CorsEndpointProperties`). Works with Spring MVC or WebFlux.

JSON: Actuator uses an isolated Jackson `JsonMapper`, unaffected by `spring.jackson.*`. Set `management.endpoints.jackson.isolated-json-mapper` to `false` to use the application's mapper, or define an `EndpointJsonMapper` bean.

## Checked

2026-11-07

Read endpoints.adoc in full (cited Actuator endpoints page); used Security, Cross Site Request Forgery Protection, Configuring Endpoints (caching), Sanitize Sensitive Values, CORS Support and JSON sections. The MySecurityConfiguration include examples were not opened; EndpointRequest claims rest on the page prose.
Confirmed: only /health exposed by default for security; auto-secured when Spring Security is present and no SecurityFilterChain bean exists, backing off when one is defined; EndpointRequest.toAnyEndpoint(); EndpointRequest.to("endpoint") matching /actuator/endpoint/**; exposure.include "*" for firewalled setups; CSRF 403 for POST (shutdown, loggers), PUT, DELETE; the non-browser-clients recommendation; sanitization of /env, /configprops, /quartz and show-values never/always/when-authorized, roles, JMX always authorized; cache.time-to-live "10s" on beans; CORS off until allowed-origins is set and the CorsEndpointProperties tip; isolated JsonMapper, management.endpoints.jackson.isolated-json-mapper, EndpointJsonMapper.
Nothing trimmed.

Method: documentation only; no commands were run.
