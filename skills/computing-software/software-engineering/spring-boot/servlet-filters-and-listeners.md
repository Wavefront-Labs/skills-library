---
id: computing-software.software-engineering.spring-boot.servlet-filters-and-listeners
name: servlet-filters-and-listeners
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, servlet, filter, filterregistrationbean, servletregistrationbean, servletcomponentscan, servletcontextinitializer]
level: practitioner
status: docs-checked
description: "Register servlets, filters and listeners as Spring beans or by scanning, control filter order, add context init parameters and use ServletContextInitializer."
sources:
  - https://docs.spring.io/spring-boot/reference/web/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With an embedded container (Tomcat or Jetty, default port 8080) you can register servlets, filters and listeners as Spring beans or by scanning.

Beans: any `Servlet`, `Filter` or servlet `*Listener` bean is registered. A single Servlet bean maps to `/`; with several, the bean name is the path prefix; filters map to `/*`. For full control use `ServletRegistrationBean`, `FilterRegistrationBean` and `ServletListenerRegistrationBean`, or the annotations `@ServletRegistration` and `@FilterRegistration`.

Filter order: usually safe to leave unordered. If needed, annotate the Filter class with `@Order` or implement `Ordered`. You cannot set the order by annotating its `@Bean` method. If you cannot change the class, define a `FilterRegistrationBean` and call `setOrder(int)` (or use the `order` attribute of `@FilterRegistration`). Avoid a filter that reads the request body at `Ordered.HIGHEST_PRECEDENCE` (it can conflict with character encoding config). A filter that wraps the request needs an order at or below `OrderedFilter.REQUEST_WRAPPER_FILTER_MAX_ORDER`.

Show every filter's order and URL patterns by setting `logging.level.web=debug`; details are logged at startup.

Filters initialize very early; if one must interact with other beans, use `DelegatingFilterProxyRegistrationBean`.

Scanning: `@ServletComponentScan` enables registration of `@WebServlet`, `@WebFilter` and `@WebListener` classes. It has no effect in a standalone container.

Context initialization: embedded containers deliberately do not run `ServletContainerInitializer` or `WebApplicationInitializer`. Register a `ServletContextInitializer` bean; its `onStartup` receives the `ServletContext` and can adapt an existing `WebApplicationInitializer`.

Init parameters: `server.servlet.context-parameters.com.example.parameter=example`.

ServletContext availability: it is set during server startup within context initialization, so beans cannot reliably get it at creation. Inject the `ApplicationContext` and access it later, or listen for `ApplicationStartedEvent`.

## Checked

2026-11-07. Read web/servlet.html in full on the live docs and compared every claim, value, property name and snippet in this skill with the page text. No corrections needed. The linked Javadoc, appendix and cross-referenced pages were not opened.

Method: read the cited page(s) in full and compared each claim with the page text; no code was run.
