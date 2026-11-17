---
id: computing-software.systems-network-administration.apache-tomcat.context-naming-and-versions
name: context-naming-and-versions
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, context, context-path, context-naming, parallel-deployment, webapp-version, root-context]
level: practitioner
status: docs-checked
description: "Map Tomcat context path and version to file base names (foo, foo#bar, ROOT, foo##42) for WARs and context XML, version ordering, and reading org.apache.catalina.webappVersion."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Context naming and versions

| Context path | Version | Context name | Base file name |
|---|---|---|---|
| `/foo` | none | `/foo` | `foo` |
| `/foo/bar` | none | `/foo/bar` | `foo#bar` |
| `""` | none | `""` | `ROOT` |
| `/foo` | 42 | `/foo##42` | `foo##42` |
| `/foo/bar` | 42 | `/foo/bar##42` | `foo#bar##42` |
| `""` | 42 | `##42` | `ROOT##42` |

- The file is `<base>.war`, `<base>.xml` or a directory `<base>`. Nested paths replace `/` with `#`; the empty path becomes `ROOT`.
- The version is appended as `##version`. Several versions of one path can run at the same time (parallel deployment): a request with no session goes to the latest version; with session information, the version whose session manager holds the session is used; if none matches, the latest version.
- Versions compare as strings: `foo.war` < `foo##11.war` < `foo##2.war`. Zero-pad (`foo##002.war`, `foo##011.war`).
- An app reads its version with:
```java
(String) request.getServletContext().getAttribute("org.apache.catalina.webappVersion");
```
- Set `undeployOldVersions="true"` on the Host to clean up superseded versions.

Under automatic deployment the context path may not be defined in a `META-INF/context.xml`; the file name defines it. To use a context path unrelated to the base file name, disable `autoDeploy` and `deployOnStartup` and define all Contexts in server.xml, or locate the WAR or directory outside the Host `appBase` and use a context XML with `docBase`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Context reference (Parallel deployment, Naming): name table, version string ordering, webappVersion attribute. Replaced the session-routing sentence and the path gotcha with the page's statements; removed the generic verify line.

Method: documentation only; no commands were run.
