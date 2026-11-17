---
id: computing-software.systems-network-administration.apache-tomcat.context-parameters-and-environment-entries
name: context-parameters-and-environment-entries
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, context, parameter, environment, env-entry, context-param, jndi, override]
level: practitioner
status: docs-checked
description: "Set context init parameters and JNDI environment entries from Tomcat 10.1 context XML with Parameter and Environment elements, plus Resource element basics."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parameter, Environment and Resource in a Context

`<Parameter>` equals web.xml `<context-param>`:
- Attributes `name`, `value`, optional `description`.
- `override="false"` stops a web.xml param of the same name replacing it (default: overridable).
```xml
<Parameter name="companyName" value="My Company" override="false"/>
```

`<Environment>` equals `<env-entry>`:
- Attributes `name` (relative to `java:comp/env`), `type` (fully qualified Java class name, a legal `<env-entry-type>`), `value` (must be convertible to the type), optional `description`.
- `override="false"` blocks web.xml override.
```xml
<Environment name="maxExemptions" value="10" type="java.lang.Integer" override="false"/>
```

`<Resource>` equals `<resource-ref>`/`<resource-env-ref>`:
- Attributes `name` (relative to `java:comp/env`), `type`. `auth` is `Application` or `Container` (required if the app uses `<resource-ref>`, optional for `<resource-env-ref>`).
- `scope`: `Shareable` or `Unshareable`; connections are assumed shareable by default.
- `singleton`: default true; must be true for a DataSource to register in JMX.
- `closeMethod`: zero-argument method called on a singleton resource when no longer required (ignored if `singleton` is false); defaults to `close` for DataSource/XADataSource implementing AutoCloseable; empty string disables; no default for other types.
```xml
<Resource name="jdbc/EmployeeDB" auth="Container" type="javax.sql.DataSource"/>
```
Real pool attributes (url, driver, limits) are in `computing-software.systems-network-administration.apache-tomcat.jdbc-datasource-resource`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Context reference (Context Parameters, Environment Entries, Resource Definitions). Dropped the "required" labels the page does not state, and removed the lookup snippet and the generic verify line.

Method: documentation only; no commands were run.
