---
id: computing-software.systems-network-administration.apache-tomcat.service-and-engine-structure
name: service-and-engine-structure
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, service, engine, defaulthost, jvmroute, startstopthreads, backgroundprocessordelay, gracefulstopawaitmillis, server-xml]
level: practitioner
status: docs-checked
description: "Tomcat 10.1 Service and Engine elements: nesting order, name uniqueness, defaultHost, jvmRoute, startStopThreads, backgroundProcessorDelay and gracefulStopAwaitMillis."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/service.html
  - https://tomcat.apache.org/tomcat-10.1-doc/config/engine.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Service and Engine

Nesting: `Server` > one or more `Service` > (Executors) + one or more `Connector`, then exactly one `Engine` > one or more `Host`.

Service:
- `name`: unique within the Server, appears in logs.
- `gracefulStopAwaitMillis` (default 0): wait for clients to finish on stop; only for Connectors with `bindOnInit="false"`.

Engine:

| Attribute | Default / rule |
|---|---|
| `name` | Must be unique when several Services exist |
| `defaultHost` | Must equal the `name` of a nested Host; serves unknown host names |
| `jvmRoute` | Appended to session IDs for load-balancer affinity; unique per node |
| `startStopThreads` | 1; 0 = CPU count; negative = CPU count + value (min 1) |
| `backgroundProcessorDelay` | 10 s; drives backgroundProcess for Engine, Hosts, Contexts |

- Only one `Realm` may be nested directly in the Engine; it is inherited by Hosts and Contexts unless overridden.
- Access logs and IP filters go in as nested `Valve` elements.
- Log category: `org.apache.catalina.core.ContainerBase.[enginename]` (brackets literal).

```xml
<Service name="Catalina">
  <Connector port="8080" protocol="HTTP/1.1" redirectPort="8443"/>
  <Engine name="Catalina" defaultHost="localhost" jvmRoute="node1">
    <Host name="localhost" appBase="webapps"/>
  </Engine>
</Service>
```

## Checked

2026-11-04. Read the Tomcat 10.1 Service (config/service.html) and Engine (config/engine.html) pages: confirmed nesting rules, name uniqueness, gracefulStopAwaitMillis, defaultHost, jvmRoute, startStopThreads, backgroundProcessorDelay 10, single nested Realm and the ContainerBase log category. Removed the startup log line, which the pages do not show.

Method: documentation only; no commands were run.
