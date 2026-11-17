---
id: computing-software.systems-network-administration.apache-tomcat.webapp-classloader-delegation
name: webapp-classloader-delegation
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, class-loader, delegate, loader-element, webapp-classloader, class-conflict, jar-hell, classnotfound]
level: advanced
status: docs-checked
description: "Tomcat 10.1 webapp class lookup order with delegate=false (default) versus <Loader delegate=true/>, plus the classes that are always delegated first."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/class-loader-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webapp class lookup order

Default (`delegate` false), first hit wins:
1. JVM bootstrap classes
2. `/WEB-INF/classes`
3. `/WEB-INF/lib/*.jar`
4. System loader classes
5. Common loader classes

With `<Loader delegate="true"/>` in the Context:
1. JVM bootstrap classes
2. System loader classes
3. Common loader classes
4. `/WEB-INF/classes`
5. `/WEB-INF/lib/*.jar`

Exceptions:
- JRE base classes cannot be overridden.
- The web app class loader always delegates first for the Jakarta EE API classes of the specifications Tomcat implements (Servlet, JSP, EL, WebSocket).
- XML parser components can be overridden using the upgradeable modules feature; overriding any JRE component carries risk.

For a class present in both the app and Common, the order above decides: the app copy is found first by default, the Common copy first with `delegate="true"`.

```xml
<Context><Loader delegate="true"/></Context>
```

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Class Loader how-to (WebappX definition and lookup orders). Reworded the always-delegated and XML parser bullets; removed the diagnosing steps, the cross-reference and the generic verify line.

Method: documentation only; no commands were run.
