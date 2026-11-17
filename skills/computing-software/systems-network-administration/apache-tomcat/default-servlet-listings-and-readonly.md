---
id: computing-software.systems-network-administration.apache-tomcat.default-servlet-listings-and-readonly
name: default-servlet-listings-and-readonly
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, default-servlet, directory-listings, listings, readonly, webdav, tomcat-web-xml, put-delete, static-content]
level: practitioner
status: docs-checked
description: "Control Tomcat 10.1 DefaultServlet: enable directory listings per app with tomcat-web.xml, readonly and allowPartialPut for PUT/DELETE, global mapping and listing XSLT."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/default-servlet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DefaultServlet: listings and write methods

The global definition in `$CATALINA_BASE/conf/web.xml` maps `org.apache.catalina.servlets.DefaultServlet` to `/` with `debug=0`, `listings=false`, `load-on-startup=1`.

Enable listings for one app without breaking portability: use `/WEB-INF/tomcat-web.xml` (Tomcat-specific, same format as web.xml, overrides global defaults but not the app's `web.xml`):
```xml
<servlet>
  <servlet-name>default</servlet-name>
  <servlet-class>org.apache.catalina.servlets.DefaultServlet</servlet-class>
  <init-param><param-name>listings</param-name><param-value>true</param-value></init-param>
</servlet>
```
Listings only appear when no welcome file is present. The page warns that listings of directories with many entries are expensive and repeated requests can consume significant server resources.

Related init-params:

| Param | Default |
|---|---|
| `listings` | false |
| `readonly` | true (PUT and DELETE rejected; false enables writes) |
| `allowPartialPut` | true (Content-Range PUT) |
| `allowPostAsGet` | true |
| `showServerInfo` | true |
| `sortListings` / `sortDirectoriesFirst` | false / false |
| `readmeFile` | readme file shown with a listing, inserted as is so it may contain HTML |
| `fileEncoding` | platform default |
| `useBomIfPresent` | true |
| `globalXsltFile`, `contextXsltFile`, `localXsltFile` | none; local overrides context overrides global |

Security: any `localXsltFile` is trusted, so restrict write access to it, including WebDAV or PUT users. Per-application security for listings is done with web.xml in each webapp.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Default Servlet Reference: global declaration, tomcat-web.xml precedence, init-param defaults, XSLT precedence and trust note. Removed the authentication advice for `readonly=false` and the generic verify line.

Method: documentation only; no commands were run.
