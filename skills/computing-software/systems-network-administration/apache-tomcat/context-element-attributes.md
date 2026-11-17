---
id: computing-software.systems-network-administration.apache-tomcat.context-element-attributes
name: context-element-attributes
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, context, reloadable, crosscontext, privileged, swallowoutput, antiresourcelocking, session-cookie, sessioncookiename, usehttponly, unloaddelay]
level: practitioner
status: docs-checked
description: "Tomcat 10.1 Context attributes with defaults: reloadable, crossContext, privileged, swallowOutput, antiResourceLocking, cookie settings, unloadDelay, allowCasualMultipartParsing."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/context.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Context attributes

| Attribute | Default | Notes |
|---|---|---|
| `reloadable` | false | true monitors `/WEB-INF/classes/` and `/WEB-INF/lib` and reloads on change; significant runtime overhead, not recommended in production |
| `crossContext` | false | Allow `ServletContext.getContext()` to other apps |
| `privileged` | not stated | Uses the Server class loader as parent (manager-style apps) |
| `swallowOutput` | false | Route System.out/err to the web app logger |
| `antiResourceLocking` | false | true prevents file locking; significantly slows startup and disables JSP reloading in a running server |
| `cookies` | true | Session cookies on |
| `sessionCookieName` | JSESSIONID | Else app/web.xml value |
| `sessionCookiePath` | app value, else context path | |
| `sessionCookieDomain` | not stated | Overrides app-set domain |
| `useHttpOnly` | true | HttpOnly session cookie |
| `unloadDelay` | 2000 ms | Wait for servlets to unload |
| `clearReferencesStopThreads` | false | Attempts to terminate app threads via Thread.stop(); last resort, not for production |
| `parallelAnnotationScanning` | false | |
| `allowCasualMultipartParsing` | false | Parse multipart even without `@MultipartConfig` |
| `validateClientProvidedNewSessionId` | true | |
| `failCtxIfServletStartFails` | Host value, else false | |

Also: `path` must be unique within a Host and `""` is the default (ROOT) app; `docBase` is absolute or relative to `appBase`.

Example:
```xml
<Context reloadable="false" sessionCookieName="APPSESSION" useHttpOnly="true"/>
```

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Context reference (common and StandardContext attributes). Rewrote the reloadable, antiResourceLocking and clearReferencesStopThreads notes to match the page; removed the Windows claim and the generic verify line.

Method: documentation only; no commands were run.
