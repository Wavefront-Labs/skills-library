---
id: computing-software.software-engineering.spring-boot.jersey-jaxrs
name: jersey-jaxrs
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, jersey, jax-rs, resourceconfig, cxf, spring-boot-starter-jersey]
level: practitioner
status: docs-checked
description: "Use Jersey or Apache CXF instead of Spring MVC: spring-boot-starter-jersey, ResourceConfig registration, servlet versus filter mode and spring.jersey.* properties."
sources:
  - https://docs.spring.io/spring-boot/reference/web/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For the JAX-RS programming model, Jersey and Apache CXF work out of the box. CXF needs its `Servlet` or `Filter` registered as a `@Bean`. Jersey has native Spring support, so Boot auto-configures it with a starter.

Start: add `spring-boot-starter-jersey` and define one `@Bean` of type `ResourceConfig` registering all endpoints.

Warning: Jersey's scanning of executable archives is limited. It cannot scan for endpoints in a package inside a fully executable jar or in `WEB-INF/classes` of an executable war. Do not use the `packages` method; register each endpoint with `register`.

Endpoints are Spring `@Component` classes with JAX-RS annotations (`@GET` and others), so Spring manages the lifecycle and you can use `@Autowired` and `@Value`. For advanced customization register any number of `ResourceConfigCustomizer` beans.

Mapping: the Jersey servlet is mapped to `/*` by default. Change it by adding `@ApplicationPath` to your `ResourceConfig`.

Registration:
- Jersey is a servlet in a `ServletRegistrationBean` bean named `jerseyServletRegistration`, initialized lazily by default; set `spring.jersey.servlet.load-on-startup` to change that.
- Disable or override the bean by creating one with the same name.
- Use a filter instead with `spring.jersey.type=filter`; the bean to replace is then `jerseyFilterRegistration`, and its order is set with `spring.jersey.filter.order`.
- In filter mode a servlet must exist to handle requests Jersey does not intercept; if there is none, set `server.servlet.register-default-servlet=true`.
- Init parameters for either registration: `spring.jersey.init.*` as a map.

## Checked

2026-11-07

Read the JAX-RS and Jersey section of servlet.adoc (docs-repo source of the cited Servlet Web Applications page, a large page of which only the sections named here were read, not all of it) in full (lines 491-524). The MyJerseyConfig and MyEndpoint include examples were not opened; claims rest on page prose.
Confirmed: Jersey and Apache CXF work out of the box, CXF needing its Servlet or Filter registered as a @Bean; Jersey native Spring support with a starter; spring-boot-starter-jersey and one ResourceConfig @Bean registering endpoints; the executable-archive scanning WARNING and the register-not-packages advice; ResourceConfigCustomizer beans; endpoints as @Component classes with @GET etc., Spring-managed lifecycle with @Autowired and @Value; servlet mapped to /* by default and @ApplicationPath on ResourceConfig; jerseyServletRegistration ServletRegistrationBean, lazy initialization and spring.jersey.servlet.load-on-startup, overriding with a same-named bean; spring.jersey.type=filter with jerseyFilterRegistration and spring.jersey.filter.order; the need for a servlet in filter mode and server.servlet.register-default-servlet=true; spring.jersey.init.* map.
Nothing trimmed.

Method: documentation only; no commands were run.
