---
id: computing-software.cybersecurity-defensive.system-hardening.tomcat-hardening
name: tomcat-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [tomcat-hardening, apache-tomcat, web-server-hardening, ajp, manager-app, java]
level: practitioner
status: docs-checked
description: "Harden Apache Tomcat: remove default webapps, lock down admin apps with RemoteCIDRValve, AJP, shutdown port, error report and version disclosure, auto-deployment."
sources: ["https://tomcat.apache.org/tomcat-10.1-doc/security-howto.html", "https://tomcat.apache.org/security.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tomcat hardening

Follow the Tomcat Security Considerations page for your branch (examples here are checked against 10.1).

## Remove defaults
Remove default web applications you do not need. The ROOT application includes the Tomcat version and should
normally be removed from a publicly accessible instance so a more appropriate default page is shown.

## Administrative applications (Manager, Host Manager)
- Protect any administrative application with a `RemoteCIDRValve` (also available as a Filter), using its `allow`
  attribute to limit access to known trusted hosts. In `context.xml` of the management application, access is
  limited to localhost by default; widen it only to specific addresses.
- Treat Manager access as administrator access, because it can deploy web applications.

## AJP connector
AJP is a clear-text protocol and AJP connectors should normally be used only on trusted networks. On an untrusted
network the shared secret limits access to authorised clients, but is visible to anyone who can observe traffic.
Leave the connector out unless a front-end proxy needs it. AJP connectors block forwarded requests with unknown
request attributes; allow known-safe ones through `allowedRequestAttributesPattern`.

## Shutdown port
`port="-1"` on the `Server` element disables the shutdown port. If it is not disabled, configure a strong shutdown
password.

## Information disclosure
- The default `ErrorReportValve` can show stack traces and JSP source (set `showReport` to `false` on an explicitly
  configured valve) and includes the Tomcat version (set `showServerInfo` to `false`), or use custom error handling
  inside each web application.
- The version number can also be changed with `CATALINA_BASE/lib/org/apache/catalina/util/ServerInfo.properties`.
- `DefaultServlet` has `showServerInfo` set to true, so directory listings include the version; set it to false on
  an explicitly configured servlet if listings are on.
- The `xpoweredBy` header is disabled by default; TRACE support (`allowTrace`) is disabled by default.

## Automatic deployment
Automatic deployment makes it easier for an attacker to deploy a malicious application. It is controlled by the
`autoDeploy` and `deployOnStartup` attributes of `Host`; if both are false, only Contexts defined in `server.xml`
are deployed and changes require a restart.

## Rewrite rules
Poorly formed regular expressions in `RewriteValve` can suffer catastrophic backtracking (ReDoS).

## Patch
Follow the Tomcat security announcements (`tomcat.apache.org/security.html`) and use a supported branch.

## Verify
No default apps respond; responses show no version; the AJP port is closed externally; administrative apps are
reachable only from the admin subnet.

## Checked
2026-10-31. Confirmed on the Tomcat 10.1 Security Considerations page: ROOT app guidance, RemoteCIDRValve with
`allow`, shutdown port `-1`, AJP clear-text and secret caveats, `allowedRequestAttributesPattern`, ErrorReportValve
`showReport`/`showServerInfo`, ServerInfo.properties, DefaultServlet `showServerInfo`, `xpoweredBy` and `allowTrace`
defaults, `autoDeploy`/`deployOnStartup`, RewriteValve ReDoS. Removed as not confirmed on that page: Ghostcat/CVE and
9.0.31 default change, AJP connector example, hashed-credential handler example, TLS protocol and RemoteIpValve
snippets, cookie and session snippets, file ownership advice, Security Manager remark, branch list, and the CIS
Tomcat benchmark claim (registration wall; source removed).
Method: documentation only; no commands were run.
