---
id: computing-software.systems-network-administration.apache-tomcat.jndi-global-resources-and-resourcelink
name: jndi-global-resources-and-resourcelink
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, jndi, globalnamingresources, resourcelink, context-resource, resource-ref, resource-env-ref, java-comp-env, closemethod, singleton]
level: practitioner
status: docs-checked
description: "Where Tomcat 10.1 JNDI resources live: web.xml references, Context Resource elements, server-wide GlobalNamingResources, java:comp/env lookups, singleton and closeMethod."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/jndi-resources-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# JNDI resources: where they go

| Location | Elements | Scope |
|---|---|---|
| `WEB-INF/web.xml` | `<env-entry>`, `<resource-ref>`, `<resource-env-ref>` | Declares needs |
| `META-INF/context.xml` or server.xml `<Context>` | `<Environment>`, `<Resource>`, `<ResourceLink>` | One web app |
| `conf/server.xml` `<GlobalNamingResources>` | `<Resource>` and similar | Whole server; expose to apps with `<ResourceLink>` |

Rules:
- A resource defined with a `<ResourceLink>` need not be defined in web.xml, but keeping the entry documents the web app's resource requirements.
- `closeMethod` (faster clean-up of JNDI resources when a web app stops) and `singleton` (whether a new instance is created for every lookup) are Tomcat-specific and cannot be specified in web.xml; the resource must be in the web app's `<Context>` or in `<GlobalNamingResources>` of `$CATALINA_BASE/conf/server.xml`.
- For the same name in a web.xml `<env-entry>` and a Context `<Environment>`, the web.xml value takes precedence only if the `<Environment>` sets `override="true"`.
- Of the standard resource factories, only "JDBC Data Source" and "User Transaction" are mandated on other platforms (and only where the platform implements the Jakarta EE specs); all other standard and custom factories are Tomcat-specific.

Lookup (the InitialContext is made available to web app components for read-only access; entries are placed under `java:comp/env`):
```java
Context envCtx = (Context) new InitialContext().lookup("java:comp/env");
DataSource ds = (DataSource) envCtx.lookup("jdbc/EmployeeDB");
```

Share a global resource: define it in `<GlobalNamingResources>` and add a `<ResourceLink>` in the per-web-app context. The link attributes are described in the Context reference, not this page.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 JNDI Resources how-to (introduction). Removed the resource-ref/auth pairing, the name-match rule, the ResourceLink snippet, `<Transaction>`, the preferred-location claim and the generic verify line.

Method: documentation only; no commands were run.
