---
id: computing-software.software-engineering.spring-boot.embedded-servlet-container-customizing
name: embedded-servlet-container-customizing
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, tomcat, jetty, embedded-server, webserverfactorycustomizer, samesite, character-encoding, jsp]
level: practitioner
status: docs-checked
description: "Customize the embedded Tomcat or Jetty: server.* properties, SameSite cookies, encoding mappings, WebServerFactoryCustomizer, direct factory beans and JSP limits."
sources:
  - https://docs.spring.io/spring-boot/reference/web/servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Common settings are Environment properties: `server.port`, `server.address`; sessions via `server.servlet.session.persistent`, `.timeout`, `.store-dir`, `.cookie.*`; error page location `spring.web.error.path`; SSL; compression. Server-specific namespaces such as `server.tomcat` cover the rest (the `ServerProperties` class lists them).

SameSite: `server.servlet.session.cookie.same-site: "none"` is supported by auto-configured Tomcat and Jetty and also configures Spring Session servlet `SessionRepository` beans. For other cookies on the `HttpServletResponse` declare a `CookieSameSiteSupplier` bean; it receives the `Cookie` and returns a SameSite value or `null`. Factory and filter methods match cookies, for example `Lax` for names matching the regex `myapp.*`.

Character encoding: `server.servlet.encoding.*`. The container maps `Accept-Language` locales to charsets with its own defaults; override with `server.servlet.encoding.mapping`, for example `ko: "UTF-8"`, equivalent to a `locale-encoding-mapping-list` entry in `web.xml`.

Programmatic: register a bean implementing `WebServerFactoryCustomizer`; it gets the `ConfigurableServletWebServerFactory` with many setters (for example the port). `TomcatServletWebServerFactory` and `JettyServletWebServerFactory` add server-specific setters.

Direct: expose your own `ServletWebServerFactory` bean for advanced cases (setters plus protected hooks). Auto-configured customizers are still applied to it, so use with care. The `ServletWebServerApplicationContext` bootstraps by searching for a single `ServletWebServerFactory` bean.

JSP limits (executable archives): work with Jetty and Tomcat using war packaging (executable war via `java -jar`, or deploy to a container); not supported with an executable jar. A custom `error.jsp` does not override the default error view; use custom error pages. With `mvn spring-boot:run` or `gradle bootRun` and a non-standard `src/main/webapp` layout you may need the `WAR_SOURCE_DIRECTORY` environment variable. JSPs should be avoided if possible.

## Checked

2026-11-07

Read the Embedded Servlet Container Support sections of servlet.adoc (docs-repo source of the cited Servlet Web Applications page, a large page of which only the sections named here were read, not all of it): ServletWebServerApplicationContext, Customizing Embedded Servlet Containers, SameSite Cookies, Character Encoding, Programmatic Customization, Customizing ConfigurableServletWebServerFactory Directly and JSP Limitations, plus the TIP at line 314 on avoiding JSPs. The MySameSiteConfiguration, MyWebServerFactoryCustomizer and MyTomcatWebServerFactoryCustomizer include examples were not opened; claims rest on page prose.
Confirmed: common settings as Environment properties (server.port, server.address, the server.servlet.session.* keys, spring.web.error.path, SSL, compression) and server.tomcat dedicated namespaces with the ServerProperties TIP; server.servlet.session.cookie.same-site "none" supported by auto-configured Tomcat and Jetty and used for Spring Session SessionRepository beans; CookieSameSiteSupplier receiving a Cookie and returning a SameSite value or null, with the Lax / myapp.* example; server.servlet.encoding.*, Accept-Language locale-to-charset mapping, server.servlet.encoding.mapping ko: "UTF-8" and the web.xml locale-encoding-mapping-list equivalence; WebServerFactoryCustomizer and ConfigurableServletWebServerFactory, TomcatServletWebServerFactory / JettyServletWebServerFactory; exposing a ServletWebServerFactory bean with setters, protected hooks and the auto-configured-customizers NOTE; ServletWebServerApplicationContext searching for a single ServletWebServerFactory bean; the three JSP limitations (war packaging, executable jar unsupported, error.jsp not overriding, WAR_SOURCE_DIRECTORY) and "JSPs should be avoided".
Nothing trimmed.

Method: documentation only; no commands were run.
