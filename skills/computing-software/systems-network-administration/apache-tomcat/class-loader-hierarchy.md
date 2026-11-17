---
id: computing-software.systems-network-administration.apache-tomcat.class-loader-hierarchy
name: class-loader-hierarchy
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, class-loader, classloader, catalina-properties, common-loader, shared-loader, server-loader, webapp-classloader, lib-directory]
level: advanced
status: docs-checked
description: "Tomcat 10.1 class loader hierarchy: Bootstrap, System, Common and Webapp loaders, common.loader lib order, optional server.loader and shared.loader, and where to put jars."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/class-loader-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Class loader hierarchy

Bootstrap > System > Common > Webapp1, Webapp2... With the advanced setup Server and Shared sit under Common and webapps under Shared.

| Loader | Loads |
|---|---|
| Bootstrap | JVM runtime classes (plus extension dir jars on old JVMs) |
| System | `bootstrap.jar`, `tomcat-juli.jar` (`$CATALINA_BASE/bin` wins over `$CATALINA_HOME/bin`), `commons-daemon.jar`; the `CLASSPATH` variable is ignored |
| Common | Paths in `common.loader` in `$CATALINA_BASE/conf/catalina.properties`; visible to Tomcat and all apps |
| Webapp | That app's `WEB-INF/classes` and `WEB-INF/lib/*.jar` |
| Server (optional) | `server.loader`; Tomcat internals only |
| Shared (optional) | `shared.loader`; all apps, not Tomcat; restart needed after changes |

Server and Shared are undefined by default (simple hierarchy).

`common.loader` order: `$CATALINA_BASE/lib` classes, `$CATALINA_BASE/lib/*.jar`, `$CATALINA_HOME/lib` classes, `$CATALINA_HOME/lib/*.jar`. Default contents include `catalina.jar`, `servlet-api.jar`, `jsp-api.jar`, `el-api.jar`, `jasper.jar`, `tomcat-coyote.jar`, `tomcat-util.jar`, `tomcat-websocket.jar`.

Practical placement:
- JDBC drivers for container pools and shared libraries: `$CATALINA_BASE/lib`.
- Application classes: inside the WAR, not in Common.
- Do not override JRE components casually; a replacement that is not fully API-compatible breaks Tomcat or the app. XML parsers: the JDK implementation is consulted first now; use upgradeable modules.
- With a security manager, the policy file also limits where classes may load from.

Verify: a `ClassNotFoundException` is resolved by locating the jar in exactly one loader; see `computing-software.systems-network-administration.apache-tomcat.webapp-classloader-delegation` for conflict order.

## Checked

2026-11-04. Read the Tomcat 10.1 Class Loader How-To (class-loader-howto.html): confirmed the Bootstrap, System, Common and Webapp definitions, tomcat-juli.jar precedence, common.loader search order and default jar list, optional server.loader and shared.loader (restart needed), the XML parser and upgradeable modules note and the security manager note. Nothing removed.

Method: documentation only; no commands were run.
