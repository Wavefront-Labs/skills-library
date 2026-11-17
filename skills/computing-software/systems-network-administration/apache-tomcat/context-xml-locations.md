---
id: computing-software.systems-network-administration.apache-tomcat.context-xml-locations
name: context-xml-locations
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, context, context-xml, meta-inf, context-xml-default, override, default-context]
level: practitioner
status: docs-checked
description: "Where to define a Tomcat 10.1 Context: META-INF/context.xml, conf/[engine]/[host]/*.xml, server.xml, and default contexts (conf/context.xml, context.xml.default) with precedence."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Where to put a Context definition

Explicit definitions:
1. `/META-INF/context.xml` inside the app. With Host `copyXML="true"` it is copied to `$CATALINA_BASE/conf/[enginename]/[hostname]/` as `<base>.xml`.
2. `$CATALINA_BASE/conf/[enginename]/[hostname]/<base>.xml`. Path and version come from the file name; it always beats `META-INF/context.xml`.
3. Inside a `<Host>` in `conf/server.xml`. The page says this is NOT recommended.

Defaults shared by many apps:
- `$CATALINA_BASE/conf/context.xml`: every web app.
- `$CATALINA_BASE/conf/[enginename]/[hostname]/context.xml.default`: every app on that host.

Precedence stated on the page:
- Per-app file in `conf/[engine]/[host]/` > `META-INF/context.xml`.
- Per-app settings > default context settings.
- A server.xml Context with `override="true"` > default context settings (otherwise defaults overwrite it).

Rules:
- Except in server.xml, each file holds a single `<Context>`.
- Nested elements (`<Resource>` and so on) in a default context are created separately for each app, not shared.
- `path` is only for a Context statically defined in server.xml; even there, set it only when `docBase` is not under the Host `appBase` or both `deployOnStartup` and `autoDeploy` are false, otherwise double deployment is likely. In all other cases the path is inferred from the file name or `docBase`.

Example `conf/Catalina/localhost/myapp.xml`:
```xml
<Context docBase="/path/to/myapp" reloadable="false"/>
```

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Context reference (Defining a context, path attribute). Corrected the `path` rule; removed the generic verify line.

Method: documentation only; no commands were run.
