---
id: computing-software.systems-network-administration.apache-tomcat.error-report-valve
name: error-report-valve
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, valve, errorreportvalve, error-pages, showreport, showserverinfo, errorcode, exceptiontype, custom-error-page]
level: practitioner
status: docs-checked
description: "Control Tomcat 10.1 error pages with ErrorReportValve: hide stack traces and server version, map status codes or exception types to custom HTML files, disable via Host attribute."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/valve.html
  - https://tomcat.apache.org/tomcat-10.1-doc/config/host.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ErrorReportValve

Class `org.apache.catalina.valves.ErrorReportValve`, used by each Host by default (Host `errorReportValveClass`).

Attributes:
- `showReport` (true): false drops the message and stack trace.
- `showServerInfo` (true): false drops the Tomcat version string.
- `errorCode.nnn`: UTF-8 HTML file for status nnn; relative paths resolve against `$CATALINA_BASE`. `errorCode.0` is the fallback.
- `exceptionType.<fully.qualified.ClassName>`: HTML file when `jakarta.servlet.error.exception` is that class or a subclass.

With both booleans false, only the status code is returned.

```xml
<Host name="localhost" appBase="webapps">
  <Valve className="org.apache.catalina.valves.ErrorReportValve"
         showReport="false" showServerInfo="false"
         errorCode.404="conf/errors/404.html"
         errorCode.0="conf/errors/generic.html"/>
</Host>
```

Alternatives:
- Host attribute `errorReportValveClass` selects another class; an empty string disables error reports entirely.
- If no matching error page is found, the default Error Report Valve response is returned.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Valve reference (Error Report Valve) and Host reference (errorReportValveClass). Removed the web.xml error-page ordering claim and the generic verify line.

Method: documentation only; no commands were run.
